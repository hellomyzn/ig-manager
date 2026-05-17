# design.md — CSV カラム整理 & 出力先変更

## 実装アプローチ

### 1. CSV 出力先変更

Docker Compose に bind mount を追加し、環境変数 `DATA_DIR` でコンテナ内パスを渡す。
`InstagramService` はモジュールレベル定数 `_DEFAULT_DATA_DIR` を環境変数から読み込む形に変更する。

```
ホスト:      ../../footprints/instagram  →  コンテナ: /opt/footprints/instagram
```

#### docker-compose.yml の変更

volumes に bind mount を追加：

```yaml
volumes:
  - type: bind
    source: ${PROJECT_DIR-./src}/
    target: ${WORKDIR-/opt/work}
  - type: bind
    source: ${FOOTPRINTS_DIR-../../footprints/instagram}
    target: /opt/footprints/instagram
```

environment に `DATA_DIR` を追加：

```yaml
environment:
  - TZ=${TZ-Asia/Tokyo}
  - DATA_DIR=/opt/footprints/instagram
```

#### .env / .env.template の変更

```
FOOTPRINTS_DIR=../../footprints/instagram
```

#### InstagramService の変更

```python
# 変更前
_DEFAULT_DATA_DIR = "data"

# 変更後
_DEFAULT_DATA_DIR = os.environ.get("DATA_DIR", "data")
```

#### Makefile の変更

`run` コマンドにホスト側ディレクトリの自動作成を追加：

```makefile
run:
	@mkdir -p ../../footprints/instagram
	@make up
	...
```

### 2. モデルのフィールド削除

常に null のフィールドをモデル・`from_dict()` ・`to_dict()` からすべて除去する。

#### InstagramMedia — 削除フィールド

`impressions` / `plays` / `video_views`

#### InstagramStory — 削除フィールド

`impressions` / `taps_forward` / `taps_back` / `exits`

#### InstagramAccount — 削除フィールド

`impressions`

#### `_SNAPSHOT_COLS`（instagram_service.py）の変更

```python
# 変更前
_SNAPSHOT_COLS = [
    "id", "fetched_at", "like_count", "comments_count",
    "reach", "impressions", "saved", "shares",
    "profile_visits", "follows", "total_interactions",
    "plays", "video_views",
]

# 変更後
_SNAPSHOT_COLS = [
    "id", "fetched_at", "like_count", "comments_count",
    "reach", "saved", "shares",
    "profile_visits", "follows", "total_interactions",
]
```

---

## 変更ファイル一覧

| ファイル | 変更内容 |
|---|---|
| `docker-compose.yml` | volume 追加・`DATA_DIR` 環境変数追加 |
| `.env` | `FOOTPRINTS_DIR` 追加 |
| `.env.template` | `FOOTPRINTS_DIR` 追加 |
| `Makefile` | `run` コマンドに `mkdir -p` 追加 |
| `src/models/instagram_media.py` | フィールド削除 |
| `src/models/instagram_story.py` | フィールド削除 |
| `src/models/instagram_account.py` | フィールド削除 |
| `src/services/instagram_service.py` | `_DEFAULT_DATA_DIR` / `_SNAPSHOT_COLS` 更新 |
| `src/tests/test_instagram_media.py` | 削除フィールドに対応 |
| `src/tests/test_instagram_story.py` | 削除フィールドに対応 |
| `src/tests/test_instagram_account.py` | 削除フィールドに対応 |
| `src/tests/test_instagram_service.py` | `_SNAPSHOT_COLS` 変更に対応 |
| `src/data/*.csv` | 削除（既存データ破棄） |
| `.gitignore` | `src/data/` を削除し `../../footprints/instagram` は対象外（別リポジトリ管理） |
| `docs/functional-design.md` | データモデル・CSV仕様・フェーズスナップショットカラム更新 |

---

## テスト戦略

既存テストから削除フィールドへの参照を除去する。新規テストは不要（既存テストの修正のみ）。

`test_instagram_service.py` の `_SNAPSHOT_COLS` 参照箇所は、削除後のカラム一覧に合わせて更新する。
