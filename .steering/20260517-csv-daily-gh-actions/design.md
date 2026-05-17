# Design: CSV日次蓄積 & GitHub Actions自動コミット

## 変更ファイル一覧

| ファイル | 変更種別 | 内容 |
|---|---|---|
| `src/services/instagram_service.py` | 修正 | フェーズロジック削除、stories削除、無条件追記に変更 |
| `src/common/csv/csv_writer.py` | 修正 | `read_last_fetched()` 削除 |
| `src/tests/test_instagram_service.py` | 修正 | 廃止ロジックのテスト削除・追記テスト追加 |
| `src/tests/test_csv_writer.py` | 修正 | `read_last_fetched` のテスト削除 |
| `.github/workflows/daily-fetch.yml` | 新規 | GitHub Actionsワークフロー |

## instagram_service.py の変更

### Before（現状）

```python
_PHASE_INTERVALS = [...]
_SNAPSHOT_COLS = [...]

def _write_medias(self, medias):
    last_fetched = read_last_fetched(snap_path, id_col="id")
    now = datetime.now(timezone.utc)
    write(media_path, [...], mode="w")
    snapshots = [snap for media in medias if self._should_snapshot(...)]
    if snapshots:
        write(snap_path, snapshots, mode="a")

def _write_stories(self, stories):
    write(path, [...], mode="w")

def _should_snapshot(self, media, last_fetched_str, now):
    ...
```

### After（変更後）

```python
_SNAPSHOT_COLS = [
    "id", "fetched_at", "like_count", "comments_count",
    "reach", "saved", "shares",
    "profile_visits", "follows", "total_interactions",
]

def _write_medias(self, medias):
    write(media_path, [m.to_dict() for m in medias], mode="w")
    snapshots = [{col: m.to_dict().get(col) for col in _SNAPSHOT_COLS} for m in medias]
    write(snap_path, snapshots, mode="a")

# _write_stories → 削除
# _should_snapshot → 削除
```

`run()` からも `_write_stories()` の呼び出しを削除。

## csv_writer.py の変更

`read_last_fetched()` 関数を削除。`instagram_service.py` からのインポートも削除。

## GitHub Actions ワークフロー設計

### ファイルパスの考え方

実行は `src/` ディレクトリから行う（config.py が相対パス `common/config/config.ini` で読む仕様のため）。

| パス | 実行時の解決先 |
|---|---|
| `common/config/config.ini` | `src/common/config/config.ini` |
| `DATA_DIR=../data` | リポジトリルートの `data/` |
| ログ | `src/logs/` |

### ワークフロー概要

```yaml
on:
  schedule:
    - cron: '0 0 * * *'   # 毎日 UTC 00:00 = JST 09:00
  workflow_dispatch:        # 手動実行（テスト用）

jobs:
  fetch:
    runs-on: ubuntu-latest
    permissions:
      contents: write       # コミット・プッシュに必要

    steps:
      - checkout
      - setup Python 3.11
      - pip install -r src/requirements.txt
      - config.ini を Secrets から生成（ENV=PROD）
      - mkdir -p data src/logs
      - cd src && DATA_DIR=../data python main.py
      - git add data/
      - 差分があればコミット＆プッシュ（差分なしはスキップ）
```

### コミットメッセージ形式

```
data: daily fetch 2026-05-17
```

### data/ ディレクトリの扱い

- `.gitignore` に `data/` は含まれていない → そのままコミット対象
- 初回実行時に `data/` が存在しなくても Actions 側で `mkdir -p data` を行う
- GitHub Actions の `GITHUB_TOKEN` を使用（追加の PAT 不要）
