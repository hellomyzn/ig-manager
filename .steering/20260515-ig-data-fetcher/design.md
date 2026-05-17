# design.md — Instagram データ取得機能

## 実装アプローチ

Instagram Graph API v21.0 に対して既存の `common/request` でHTTPリクエストを行い、取得データを dataclass モデルに格納してローカル CSV に書き出す。
Controller → Service → Repository → Accessor の層構造で処理する。

---

## ディレクトリ構成（追加・変更分のみ）

```
src/
├── common/
│   ├── csv/
│   │   ├── __init__.py
│   │   └── csv_writer.py            # CSV 読み書き共通処理
│   └── instagram/
│       ├── __init__.py
│       └── instagram_accessor.py    # API クライアント（認証・リクエスト共通処理）
├── models/
│   ├── instagram_media.py           # 投稿モデル（基本情報 + インサイト）
│   ├── instagram_story.py           # ストーリーズモデル
│   └── instagram_account.py        # アカウントモデル
├── repositories/
│   └── instagram_repository.py     # API 呼び出し → モデル変換
├── services/
│   └── instagram_service.py        # フロー制御・フェーズ判定・CSV書き出し
├── controllers/
│   └── instagram_controller.py     # エントリポイント
├── data/                            # 出力先（.gitignore 対象）
│   ├── media.csv
│   ├── media_snapshots.csv
│   ├── stories.csv
│   └── account_snapshots.csv
└── common/config/
    └── config.template.ini          # [INSTAGRAM] セクション追加（更新）
```

---

## API 呼び出し設計

ベースURL: `https://graph.facebook.com/v21.0/`

### A. 投稿（Media）

| # | エンドポイント | 目的 |
|---|---|---|
| 1 | `GET /{user_id}/media` | 全投稿の基本情報一覧（ページング） |
| 2 | `GET /{media_id}/insights` | 各投稿のインサイト |

**①のフィールド**
```
id,timestamp,caption,media_type,media_product_type,
permalink,media_url,thumbnail_url,
like_count,comments_count,is_comment_enabled
```

**②のメトリクス**
- 通常投稿・カルーセル: `reach,impressions,saved,shares,profile_visits,follows,total_interactions`
- リール（media_product_type=REELS）: 上記 + `plays,video_views`

ページング: `cursor` ベースで `after` カーソルが無くなるまでループして全件取得

### B. ストーリーズ（Stories）

| # | エンドポイント | 目的 |
|---|---|---|
| 1 | `GET /{user_id}/stories` | アクティブストーリー一覧 |
| 2 | `GET /{story_id}/insights` | 各ストーリーのインサイト |

**①のフィールド**: `id,timestamp,media_url,permalink`

**②のメトリクス**: `reach,impressions,replies,taps_forward,taps_back,exits`

### C. アカウント（User）

| # | エンドポイント | 目的 |
|---|---|---|
| 1 | `GET /{user_id}` | アカウント基本情報 |
| 2 | `GET /{user_id}/insights` | 日次インサイト |

**①のフィールド**: `username,biography,followers_count,follows_count,media_count`

**②のパラメータ**: `metric=impressions,reach,profile_views,website_clicks` / `period=day`

---

## データモデル定義

### `models/instagram_media.py`

```python
@dataclass
class InstagramMedia(Model):
    id: str
    timestamp: str
    caption: Optional[str]
    media_type: str                  # IMAGE / VIDEO / CAROUSEL_ALBUM
    media_product_type: str          # FEED / REELS
    permalink: str
    media_url: Optional[str]
    thumbnail_url: Optional[str]
    like_count: int
    comments_count: int
    is_comment_enabled: bool
    hashtags: list[str]              # caption から自動抽出
    reach: Optional[int]
    impressions: Optional[int]
    saved: Optional[int]
    shares: Optional[int]
    profile_visits: Optional[int]
    follows: Optional[int]
    total_interactions: Optional[int]
    plays: Optional[int]             # リール専用
    video_views: Optional[int]       # リール専用
    fetched_at: str                  # 取得日時（ISO8601）
```

### `models/instagram_story.py`

```python
@dataclass
class InstagramStory(Model):
    id: str
    timestamp: str
    media_url: Optional[str]
    permalink: Optional[str]
    reach: Optional[int]
    impressions: Optional[int]
    replies: Optional[int]
    taps_forward: Optional[int]
    taps_back: Optional[int]
    exits: Optional[int]
    fetched_at: str
```

### `models/instagram_account.py`

```python
@dataclass
class InstagramAccount(Model):
    username: str
    biography: Optional[str]
    followers_count: int
    follows_count: int
    media_count: int
    impressions: Optional[int]
    reach: Optional[int]
    profile_views: Optional[int]
    website_clicks: Optional[int]
    fetched_at: str
```

---

## 各クラスの責務

### `common/instagram/instagram_accessor.py`
- アクセストークンと user_id を保持するシングルトン
- `get(path, params)` で `common.request.get` を呼び出す
- `parse_insights(response)` — Insights API レスポンスを `{"reach": 1234, ...}` に変換

```python
# Insights レスポンス形式
# {"data": [{"name": "reach", "values": [{"value": 1234}]}, ...]}
# → {"reach": 1234, ...} に変換
```

### `common/csv/csv_writer.py`
- `write(filepath, rows, mode)` — `mode="w"` で上書き、`mode="a"` で追記
- ヘッダ行の有無を自動判定（追記時はファイルが空の場合のみヘッダを書く）
- モデルの `to_dict()` の結果をそのまま受け取れるインターフェース

### `repositories/instagram_repository.py`
- `fetch_medias() -> list[InstagramMedia]` — 全投稿をページング取得しインサイトをマージ。ハッシュタグは `re.findall(r'#\w+', caption)` で抽出
- `fetch_stories() -> list[InstagramStory]`
- `fetch_account() -> InstagramAccount`

### `services/instagram_service.py`
- `run()` — メイン処理を以下の順で実行：
  1. repository で全データ取得
  2. **フェーズ判定**：`media_snapshots.csv` を読み込み、各投稿の最終取得日時を確認。投稿の age と最終取得からの経過時間からスナップショット追記が必要かを判定
  3. `data/media.csv` を全件上書き
  4. スナップショット対象の投稿を `data/media_snapshots.csv` に追記
  5. `data/stories.csv` を全件上書き
  6. `data/account_snapshots.csv` に追記

### `controllers/instagram_controller.py`
- `run()` — `instagram_service.run()` を呼び出しログ出力

---

## フェーズ判定ロジック

`media_snapshots.csv` から `(post_id, fetched_at)` の最終レコードを読み取り、以下で判定：

```
post_age    = now - post.timestamp        # 投稿からの経過時間
last_fetch  = now - last_fetched_at       # 最終取得からの経過時間

フェーズ1（初速）: post_age <= 1h   → last_fetch >= 15min でスナップショット追記
フェーズ2（初日）: post_age <= 24h  → last_fetch >= 1h  でスナップショット追記
フェーズ3（初週）: post_age <= 7d   → last_fetch >= 24h でスナップショット追記
フェーズ4（安定）: post_age > 7d    → last_fetch >= 7d  でスナップショット追記
初回取得（snapshots未記録）         → 無条件でスナップショット追記
```

---

## CSV ファイル仕様

### `data/media.csv`（全件上書き）
全フィールドをカラムとして出力。`hashtags` はカンマ区切り文字列で格納。

### `data/media_snapshots.csv`（追記）
| カラム | 説明 |
|---|---|
| id | 投稿ID |
| fetched_at | 取得日時 |
| like_count, comments_count | 基本数値 |
| reach, impressions, saved, shares, profile_visits, follows, total_interactions | インサイト |
| plays, video_views | リール専用（非リールは空） |

### `data/stories.csv`（全件上書き）
全フィールドをカラムとして出力。

### `data/account_snapshots.csv`（追記）
全フィールドをカラムとして出力。

---

## 設定（config.template.ini 追記）

```ini
[INSTAGRAM]
ACCESS_TOKEN=
USER_ID=
API_VERSION=v21.0
```

---

## エラーハンドリング方針

- HTTP エラー → `common/request.get` のリトライ機構（デフォルト3回）に委任
- 個別投稿/ストーリーのインサイト取得失敗 → `warn` ログを出してスキップ（`None` のままモデル生成、全体処理は継続）
- アカウント情報の取得失敗 → `error_stack_trace` 後に例外を再スロー

---

## 影響範囲

| ファイル | 変更種別 |
|---|---|
| `src/common/csv/__init__.py` | 新規作成 |
| `src/common/csv/csv_writer.py` | 新規作成 |
| `src/common/instagram/__init__.py` | 新規作成 |
| `src/common/instagram/instagram_accessor.py` | 新規作成 |
| `src/models/instagram_media.py` | 新規作成 |
| `src/models/instagram_story.py` | 新規作成 |
| `src/models/instagram_account.py` | 新規作成 |
| `src/repositories/instagram_repository.py` | 新規作成 |
| `src/services/instagram_service.py` | 新規作成 |
| `src/controllers/instagram_controller.py` | 新規作成 |
| `src/common/config/config.template.ini` | 更新（[INSTAGRAM] セクション追加） |
| `src/main.py` | 更新（instagram_controller.run() 呼び出し） |
| `.gitignore` | 更新（`src/data/` を追加） |
