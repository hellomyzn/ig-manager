# design.md — 設計ドキュメント作成

## 実装アプローチ

既存の実装コードを正とし、各ドキュメントに記述する内容を以下の通り定義する。
`docs/dev/` 以下の旧ドキュメントは内容を統合・整理したうえで削除する。

---

## 各ドキュメントの内容定義

### `docs/product-requirements.md`

| セクション | 内容 |
|---|---|
| プロダクトビジョン | Instagram データをローカル CSV に蓄積し、パフォーマンス分析を自動化する |
| ターゲットユーザー | Instagram アカウント運用者（個人） |
| 主要機能 | メディア取得・ストーリー取得・アカウント取得・CSV 出力・フェーズスナップショット |
| ユーザーストーリー | `make run` 一発で4つの CSV が更新される |
| 受け入れ条件 | media.csv / media_snapshots.csv / stories.csv / account_snapshots.csv が正しく生成される |

### `docs/functional-design.md`

| セクション | 内容 |
|---|---|
| アーキテクチャ | Controller → Service → Repository → Accessor の4層構成（Mermaid 図） |
| コンポーネント設計 | 各クラスの責務・依存関係 |
| データモデル | InstagramMedia / InstagramStory / InstagramAccount の全フィールド定義 |
| CSV 仕様 | 4ファイルの出力仕様（上書き vs 追記、カラム一覧） |
| フェーズスナップショット仕様 | 投稿経過時間に応じた取得間隔テーブル |
| Instagram API 制約 | v22.0〜v25.0 での廃止メトリクス一覧 |

### `docs/architecture.md`

| セクション | 内容 |
|---|---|
| 技術スタック | Python 3.11 / Docker / requests / tenacity |
| 開発環境 | Docker Compose（make run / make test） |
| ディレクトリ構成（src/） | レイヤー構成の概要 |
| 設定ファイル | config.ini / config.template.ini の構造 |
| 技術的制約 | Instagram Graph API v25.0 の制限事項 |

### `docs/repository-structure.md`

| セクション | 内容 |
|---|---|
| ルートレベル | Makefile / docker-compose.yml / .gitignore 等の説明 |
| src/ 配下 | controllers / services / repositories / models / common / tests の役割 |
| docs/ / .steering/ | 各ディレクトリの用途 |
| gitignore 対象 | config.ini / src/data/ / ログなど |

### `docs/development-guidelines.md`

`docs/dev/development.md` の内容を整理・更新して統合する。

| セクション | 内容 |
|---|---|
| コーディング規約 | dataclass ベース、型ヒント必須、コメントは WHY のみ |
| テスト規約 | TDD、`make test` で全テスト実行、mock は外部 API のみ |
| 実行コマンド | `make run` / `make test` |
| Git 規約 | コミットプレフィックス（add / update / delete / fix） |
| パッケージ管理 | poetry で管理、requirements.txt はエクスポート成果物 |

### `docs/glossary.md`

| 用語 | 定義 |
|---|---|
| メディア（Media） | Instagram の投稿（画像・動画・リール） |
| リール（Reels） | media_product_type = "REELS" の投稿 |
| ストーリー（Story） | 24時間で消えるコンテンツ |
| インサイト（Insights） | リーチ・保存数などのエンゲージメント指標 |
| フェーズスナップショット | 投稿経過時間に応じた間引き取得ロジック |
| スナップショット（Snapshot） | 特定時点のエンゲージメント指標の記録 |

---

## 旧ドキュメントの扱い

| ファイル | 対応 |
|---|---|
| `docs/dev/development.md` | Git 規約・パッケージ管理を `development-guidelines.md` に統合後、削除 |
| `docs/dev/design.md` | PlantUML の使い方メモのみで設計資料でないため削除 |
| `docs/dev/` ディレクトリ | 上記削除後に空になるため削除 |

---

## ファイル配置

```
docs/
├── product-requirements.md   （新規作成）
├── functional-design.md      （新規作成）
├── architecture.md           （新規作成）
├── repository-structure.md   （新規作成）
├── development-guidelines.md （新規作成）
├── glossary.md               （新規作成）
├── images/
│   ├── git-flow.png          （保持）
│   ├── plantuml_export.png   （保持）
│   └── plantuml_preview.png  （保持）
└── sphinx/                   （既存のまま保持）
```
