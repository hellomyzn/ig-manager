# Tasklist: CSV日次蓄積 & GitHub Actions自動コミット

## タスク一覧

### 1. instagram_service.py の簡素化
- [x] `_PHASE_INTERVALS` 定数を削除
- [x] `read_last_fetched` のインポートを削除
- [x] `_write_medias()` を全投稿無条件追記に書き換え
- [x] `_write_stories()` メソッドを削除
- [x] `run()` から `_write_stories()` 呼び出しを削除
- [x] `_should_snapshot()` メソッドを削除
- [x] 不要になった `datetime` / `timedelta` / `timezone` のインポートを削除

### 2. csv_writer.py の簡素化
- [x] `read_last_fetched()` 関数を削除

### 3. テストの更新
- [x] `test_csv_writer.py` から `read_last_fetched` 関連テストを削除
- [x] `test_instagram_service.py` から `_should_snapshot` / stories 関連テストを削除
- [x] `test_instagram_service.py` に無条件追記の動作テストを追加

### 4. GitHub Actions ワークフロー作成
- [x] `.github/workflows/` ディレクトリ作成
- [x] `daily-fetch.yml` を作成（cron / checkout / setup / config生成 / 実行 / commit-push）

### 5. 動作確認
- [x] `pytest` がパスすること（55 passed）
