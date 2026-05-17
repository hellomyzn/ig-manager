# tasklist.md — CSV カラム整理 & 出力先変更

## タスク一覧

### 1. Docker / インフラ設定
- [x] `docker-compose.yml` に bind mount と `DATA_DIR` 環境変数を追加
- [x] `.env` に `FOOTPRINTS_DIR=../../footprints/instagram` を追加
- [x] `.env.template` に `FOOTPRINTS_DIR=../../footprints/instagram` を追加
- [x] `Makefile` の `run` コマンドに `mkdir -p ../../footprints/instagram` を追加

### 2. サービス更新
- [x] `src/services/instagram_service.py` の `_DEFAULT_DATA_DIR` を環境変数から読み込むよう変更
- [x] `src/services/instagram_service.py` の `_SNAPSHOT_COLS` から削除フィールドを除去

### 3. モデル更新
- [x] `src/models/instagram_media.py` から `impressions` / `plays` / `video_views` を削除
- [x] `src/models/instagram_story.py` から `impressions` / `taps_forward` / `taps_back` / `exits` を削除
- [x] `src/models/instagram_account.py` から `impressions` を削除

### 4. テスト更新
- [x] `src/tests/test_instagram_media.py` を削除フィールドに対応
- [x] `src/tests/test_instagram_story.py` を削除フィールドに対応
- [x] `src/tests/test_instagram_account.py` を削除フィールドに対応
- [x] `src/tests/test_instagram_service.py` を `_SNAPSHOT_COLS` 変更に対応

### 5. 既存データ・設定整理
- [x] `src/data/*.csv` を削除
- [x] `.gitignore` の `src/data/` を削除（footprints は別管理）

### 6. ドキュメント更新
- [x] `docs/functional-design.md` のデータモデル・CSV仕様・スナップショットカラムを更新

### 7. 動作確認
- [x] `make test` が通ること（53 passed）

## 完了条件
- [x] 全タスク完了
- [x] `make test` がグリーン
