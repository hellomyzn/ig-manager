# requirements.md — GitHub パブリック公開準備

## 概要

リポジトリを GitHub にパブリック公開するにあたり、不要ファイルの整理・セキュリティ確認・`.gitignore` の整備を行う。

## ユーザーストーリー

- 開発者として、リポジトリを安全にパブリック公開できる状態にしたい
- 見る人が混乱しないよう、不要なサンプルファイルや未使用コードを整理したい

## 受け入れ条件

- [ ] 秘密情報（アクセストークン、APIキーなど）がコミットされていない
- [ ] 不要なサンプルファイル・未使用コードが削除されている
- [ ] `.gitignore` が必要なファイルを正しく除外している
- [ ] `make test` が引き続き通る

## 対象

### セキュリティ確認済み（対応不要）

- `src/common/config/config.ini` → gitignore 済み ✓
- `.env` 系ファイル → gitignore 済み ✓
- `src/data/*.csv` → gitignore 済み ✓
- `src/src/logs/dev.log` → gitignore 済み ✓

### 削除・整理の候補

1. **不要な画像** — `docs/images/wakatime_api_key.png` など、プロジェクトと無関係なスクリーンショット
2. **サンプルコード** — `src/controllers/sample_controller.py`, `src/services/sample_service.py`, `src/models/sample.py`, `src/repositories/sample_repository.py`, `src/repositories/sample_repository_interface.py`, `src/tests/test_sample.py` など、ig-manager の機能と無関係なテンプレート残滓
3. **未使用の共通モジュール** — `src/common/google_spreadsheet/`, `src/common/spotify/`, `src/common/ssh/` など、現在の実装で使われていないアクセサ
4. **Sphinx ドキュメント** — `docs/sphinx/` 未使用ならば整理
5. **`src/src/` ディレクトリ** — 二重 src の構造が不明瞭（内部に json/.gitkeep, logs/.gitkeep のみ）

## 制約事項

- `make test` が通ること
- `make run` が引き続き動作すること
- 削除前に各ファイルが本当に未使用であることを確認する
