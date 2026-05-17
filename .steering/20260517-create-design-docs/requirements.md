# requirements.md — 設計ドキュメント作成

## 概要

CLAUDE.md で定義された永続的ドキュメント（`docs/`）が存在しないため、ig-manager の実装内容に基づいて設計資料を整備する。
GitHub パブリック公開にあたり、リポジトリを見た人がプロジェクトの目的・設計・構造を把握できる状態にする。

## ユーザーストーリー

- 開発者として、ig-manager の目的・アーキテクチャ・データ構造を一箇所で確認したい
- 将来の機能追加時に、設計方針の参照先が欲しい

## 作成するドキュメント

CLAUDE.md の定義に従い、以下の6ファイルを `docs/` 直下に作成する。

| ファイル | 内容 |
|---|---|
| `docs/product-requirements.md` | プロダクトビジョン・ユーザーストーリー・受け入れ条件 |
| `docs/functional-design.md` | アーキテクチャ・データモデル・コンポーネント設計・CSV 仕様 |
| `docs/architecture.md` | 技術スタック・開発環境・技術的制約 |
| `docs/repository-structure.md` | フォルダ・ファイル構成と役割 |
| `docs/development-guidelines.md` | コーディング規約・テスト規約・Git 規約 |
| `docs/glossary.md` | ドメイン用語定義・英日対応表 |

## 既存ドキュメントの扱い

- `docs/dev/development.md` — Git フロー・パッケージ管理などを `development-guidelines.md` に統合後、削除
- `docs/dev/design.md` — PlantUML の使い方メモのみで設計情報がないため削除
- `docs/dev/` ディレクトリ — 上記削除後に不要となるため削除

## 受け入れ条件

- [ ] 6ファイルが `docs/` 直下に作成されていること
- [ ] 各ドキュメントが実装済みの内容（Instagram API v25.0、CSV 出力、フェーズ判定など）を正確に記述していること
- [ ] `docs/dev/` が整理されていること
