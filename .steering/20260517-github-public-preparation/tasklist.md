# tasklist.md — GitHub パブリック公開準備

## タスク一覧

### 1. サンプルコード削除
- [x] `src/tests/test_sample.py` 削除
- [x] `src/controllers/sample_controller.py` 削除
- [x] `src/services/sample_service.py` 削除
- [x] `src/models/sample.py` 削除
- [x] `src/repositories/sample_repository.py` 削除
- [x] `src/repositories/sample_repository_interface.py` 削除
- [x] `src/repositories/model_adapter.py` 削除

### 2. __init__.py 整理
- [x] `src/models/__init__.py` から `from .sample import Sample` を削除
- [x] `src/repositories/__init__.py` から `from .model_adapter import ModelAdapter` を削除

### 3. 未使用共通モジュール削除
- [x] `src/common/google_spreadsheet/` ディレクトリ削除
- [x] `src/common/spotify/` ディレクトリ削除
- [x] `src/common/ssh/` ディレクトリ削除
- [x] `src/common/request/` ディレクトリ削除
- [x] `src/common/retry/` ディレクトリ削除
- [x] `src/common/decorator/` ディレクトリ削除
- [x] `src/common/exceptions/` ディレクトリ削除

### 4. 不要ドキュメント・画像削除
- [x] `docs/images/start_vscode.png` 削除
- [x] `docs/images/wakatime_api_key.png` 削除
- [x] `docs/sequences/sample.pu` 削除
- [x] `docs/sequences/sample.svg` 削除
- [x] `docs/design/db/sample_db.md` 削除

### 5. config ファイル整理
- [x] `src/common/config/config.template.ini` から `[SPOTIPY]` / `[GSS]` セクション削除
- [x] `src/common/config/config.test.ini` から `[SPOTIPY]` / `[GSS]` セクション削除

### 6. 依存パッケージ整理
- [x] `src/pyproject.toml` から `gspread` / `oauth2client` / `paramiko` を削除し `requests` を追加
- [x] `src/requirements.txt` から Google / SSH / Spotify 関連パッケージを削除（`requests` / `tenacity` は保持）

### 7. 動作確認
- [x] `make test` が通ること（53 passed）

## 完了条件
- [x] 全タスク完了
- [x] `make test` がグリーン
