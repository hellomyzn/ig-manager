# design.md — GitHub パブリック公開準備

## 実装アプローチ

不要ファイルを削除し、`__init__.py` の import を整理する。
削除後に `make test` を実行して既存テストが通ることを確認する。

---

## 削除対象ファイル

### 1. サンプルコード（テンプレート残滓）

| ファイル | 理由 |
|---|---|
| `src/controllers/sample_controller.py` | ig-manager で未使用 |
| `src/services/sample_service.py` | ig-manager で未使用 |
| `src/models/sample.py` | ig-manager で未使用 |
| `src/repositories/sample_repository.py` | ig-manager で未使用 |
| `src/repositories/sample_repository_interface.py` | ig-manager で未使用 |
| `src/repositories/model_adapter.py` | sample_repository からのみ参照 |
| `src/tests/test_sample.py` | sample コードのテスト |

### 2. 未使用の共通モジュール

下記モジュールは ig-manager の実装（Instagram 機能）から一切参照されていない。
また、相互依存もすべてサンプルコードまたは削除対象モジュール内に閉じている。

| ディレクトリ | 理由 |
|---|---|
| `src/common/google_spreadsheet/` | 未使用（CSV 出力に切り替え済み） |
| `src/common/spotify/` | 未使用 |
| `src/common/ssh/` | 未使用 |
| `src/common/request/` | `sample_service.py` からのみ参照 |
| `src/common/retry/` | `common/request/` からのみ参照 |
| `src/common/decorator/` | `sample_service.py` からのみ参照 |
| `src/common/exceptions/` | `ssh_accessor.py` と `decorator/exception_deco.py` からのみ参照（両方削除対象） |

### 3. 不要なドキュメント・画像

| ファイル | 理由 |
|---|---|
| `docs/images/start_vscode.png` | ドキュメント内に参照なし |
| `docs/images/wakatime_api_key.png` | ドキュメント内に参照なし |
| `docs/sequences/sample.pu` | サンプル PlantUML |
| `docs/sequences/sample.svg` | サンプル PlantUML |
| `docs/design/db/sample_db.md` | サンプル DB 設計 |

> `git-flow.png` / `plantuml_export.png` / `plantuml_preview.png` は `docs/dev/` から参照されているため保持。

---

## 更新が必要なファイル

| ファイル | 変更内容 |
|---|---|
| `src/models/__init__.py` | `from .sample import Sample` を削除 |
| `src/repositories/__init__.py` | `from .model_adapter import ModelAdapter` を削除 |

---

## 依存関係図（削除後）

```
src/common/
├── config/        ← InstagramAccessor が使用（保持）
├── csv/           ← InstagramService が使用（保持）
├── instagram/     ← InstagramRepository が使用（保持）
└── log/           ← main.py が使用（保持）
```

削除後に残る `src/common/` は上記4モジュールのみ。

---

## 影響範囲

- `make test` への影響：`test_sample.py` が削除されるがその他のテストは無影響
- `make run` への影響：なし（削除対象はいずれも `main.py` から呼ばれていない）
- `docs/` への影響：参照のある画像はすべて保持

---

## 対応しないもの（スコープ外）

以下は今回の整理対象としない（コンテンツとして正当性があるため）：

- `docs/dev/development.md` / `docs/dev/design.md` — 開発標準ドキュメントとして保持
- `docs/sphinx/` — 削除しても構わないが優先度低、今回は残す
- `.devcontainer/` — Dev Container 設定として保持
- `src/src/` — gitignore 済み、`.gitkeep` のみコミット対象、今回は残す
