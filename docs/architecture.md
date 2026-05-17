# architecture.md — 技術仕様書

## 技術スタック

| カテゴリ | 技術 | バージョン |
|---|---|---|
| 言語 | Python | 3.11 |
| コンテナ | Docker / Docker Compose | - |
| HTTP クライアント | requests | ^2.31.0 |
| リトライ | tenacity | ^9.0.0 |
| テスト | pytest / pytest-cov | ^8.0.2 / ^4.1.0 |
| パッケージ管理 | Poetry | - |
| 外部 API | Instagram Graph API | v25.0 |

## 開発環境

すべての実行は Docker コンテナ内で行う。ローカルに Python 環境は不要。

```
make run    # データ取得・CSV 出力
make test   # テスト実行
make up     # コンテナ起動のみ
```

Docker Compose でコンテナを起動し、`workspace` サービス内で Python を実行する。

## 設定ファイル

`src/common/config/config.ini`（gitignore 対象）に実値を設定する。テンプレートは `config.template.ini`。

```ini
[APP]
ENV=PRO

[LOG]
NAME = pro
PATH = ./src/logs/production.log
LEVEL = INFO

[INSTAGRAM]
ACCESS_TOKEN=  # Instagram Graph API の長期アクセストークン
USER_ID=       # Instagram ビジネスアカウントの User ID
API_VERSION=v25.0
```

`Config` クラスは Singleton で実装されており、アプリケーション起動時に一度だけ読み込まれる。

## ディレクトリ構成（src/）

```
src/
├── main.py                      # エントリポイント
├── controllers/                 # リクエスト受付・エラーハンドリング
├── services/                    # フロー制御・ビジネスロジック
├── repositories/                # API 呼び出し・モデル変換
├── models/                      # データモデル（dataclass）
├── common/
│   ├── config/                  # 設定ファイル読み込み（Singleton）
│   ├── csv/                     # CSV 読み書きユーティリティ
│   ├── instagram/               # Instagram API クライアント（Singleton）
│   └── log/                     # ログユーティリティ
├── utils/
│   ├── singleton.py             # Singleton 基底クラス
│   └── datetime_parser.py       # 日時パースユーティリティ
├── tests/                       # pytest テスト
├── data/                        # CSV 出力先（gitignore 対象）
├── pyproject.toml               # Poetry 設定・pytest 設定
├── requirements.txt             # 本番依存パッケージ
└── requirements-dev.txt         # 開発依存パッケージ
```

## 技術的制約

- **Instagram Graph API v25.0** — 廃止メトリクスが複数存在する（詳細は `functional-design.md` 参照）
- **アクセストークンの有効期限** — 長期トークンでも約60日で失効する。失効時は Meta Developer Portal で再発行が必要
- **`instagram_manage_insights` スコープ** — Graph API Explorer のドロップダウンには表示されない。手動 OAuth フローで取得する必要がある
- **API レートリミット** — tenacity により接続エラー時のみリトライ（最大3回、10秒待機）。HTTP 4xx エラーはリトライしない
