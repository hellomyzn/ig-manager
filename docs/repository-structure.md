# repository-structure.md — リポジトリ構造定義書

## ルートレベル

```
ig-manager/
├── .devcontainer/               # VS Code Dev Container 設定
├── .steering/                   # 作業単位の設計ドキュメント（履歴として保持）
├── docs/                        # 永続的設計ドキュメント
├── infra/
│   └── docker/python/           # Docker イメージ定義
├── src/                         # アプリケーションコード
├── .env                         # 環境変数（gitignore 対象）
├── .env.template                # 環境変数テンプレート
├── .gitignore
├── CLAUDE.md                    # Claude Code 向けプロジェクト指示
├── Makefile                     # 実行コマンド定義
├── README.md
├── TODO.md
└── docker-compose.yml           # コンテナ構成定義
```

## docs/ — 永続的ドキュメント

アプリケーション全体の設計を定義する恒久的なドキュメント。

```
docs/
├── product-requirements.md      # プロダクト要求定義書
├── functional-design.md         # 機能設計書
├── architecture.md              # 技術仕様書
├── repository-structure.md      # リポジトリ構造定義書（本ファイル）
├── development-guidelines.md    # 開発ガイドライン
├── glossary.md                  # ユビキタス言語定義
├── images/                      # ドキュメント用画像
└── sphinx/                      # Sphinx ドキュメント生成設定
```

## .steering/ — 作業単位のドキュメント

特定の開発作業ごとに作成するステアリングファイル。作業完了後も履歴として保持する。

```
.steering/
└── YYYYMMDD-[開発タイトル]/
    ├── requirements.md          # 作業の要求内容
    ├── design.md                # 変更内容の設計
    └── tasklist.md              # タスクリストと進捗
```

## src/ — アプリケーションコード

```
src/
├── main.py                      # エントリポイント
│
├── controllers/                 # エントリポイントレイヤー
│   └── instagram_controller.py  # Service 呼び出し・エラーハンドリング
│
├── services/                    # ビジネスロジックレイヤー
│   └── instagram_service.py     # フロー制御・フェーズ判定・CSV 書き出し
│
├── repositories/                # データアクセスレイヤー
│   └── instagram_repository.py  # API 呼び出し・モデル変換・ページング
│
├── models/                      # データモデル
│   ├── model.py                 # 抽象基底クラス
│   ├── instagram_media.py       # 投稿モデル
│   ├── instagram_story.py       # ストーリーモデル
│   └── instagram_account.py     # アカウントモデル
│
├── common/                      # 共通モジュール
│   ├── config/                  # 設定ファイル読み込み（Singleton）
│   ├── csv/                     # CSV 読み書きユーティリティ
│   ├── instagram/               # Instagram Graph API クライアント（Singleton）
│   └── log/                     # ログユーティリティ
│
├── utils/
│   ├── singleton.py             # Singleton 基底クラス
│   └── datetime_parser.py       # 日時パースユーティリティ
│
├── tests/                       # pytest テストスイート
│   ├── conftest.py              # フィクスチャ定義（Singleton リセット）
│   ├── test_csv_writer.py
│   ├── test_instagram_accessor.py
│   ├── test_instagram_account.py
│   ├── test_instagram_controller.py
│   ├── test_instagram_media.py
│   ├── test_instagram_repository.py
│   ├── test_instagram_service.py
│   └── test_instagram_story.py
│
├── data/                        # CSV 出力先（gitignore 対象）
│   ├── media.csv
│   ├── media_snapshots.csv
│   ├── stories.csv
│   └── account_snapshots.csv
│
├── common/config/
│   ├── config.ini               # 実値設定（gitignore 対象）
│   ├── config.template.ini      # テンプレート（コミット対象）
│   └── config.test.ini          # テスト用設定（ダミー値）
│
├── pyproject.toml               # Poetry 設定・pytest 設定
├── requirements.txt             # 本番依存パッケージ
└── requirements-dev.txt         # 開発依存パッケージ
```

## ファイル配置ルール

| 種別 | 配置先 |
|---|---|
| 新しいデータ取得機能 | controllers / services / repositories / models に1ファイルずつ |
| 共通ユーティリティ | `src/common/<機能名>/` ディレクトリを作成 |
| テスト | `src/tests/test_<対象ファイル名>.py` |
| 設計ドキュメント | `docs/` または `.steering/YYYYMMDD-*/` |

## gitignore 対象

| パス | 理由 |
|---|---|
| `src/common/config/config.ini` | アクセストークン等の秘密情報 |
| `src/data/` | 取得した Instagram データ（個人情報） |
| `.env` / `.devcontainer/.env` / `.vscode/.env` | 環境変数 |
| `src/src/logs/` 内のログファイル | 実行ログ（トークン等が含まれる可能性） |
| `__pycache__/` / `*.pyc` / `.pytest_cache/` | Python キャッシュ |
