# development-guidelines.md — 開発ガイドライン

## 実行コマンド

```bash
make run    # データ取得・CSV 出力
make test   # テスト実行（Docker コンテナ内）
make up     # コンテナ起動のみ
```

すべての Python 実行は Docker コンテナ内で行う。ローカルへの Python インストールは不要。

## コーディング規約

- **dataclass** を基本のデータ構造として使用する
- **型ヒント**を必ず付与する（`Optional[int]` 等）
- **コメント**は WHY（なぜそうするか）のみ記述する。WHAT はコードで表現する
- モデルは `from_dict()` / `to_dict()` / `to_json()` を実装する（`Model` 抽象クラスに準拠）
- Singleton パターンは `utils/singleton.py` の `Singleton` 基底クラスを継承して実装する

## 命名規則

| 対象 | 規則 | 例 |
|---|---|---|
| クラス | PascalCase | `InstagramRepository` |
| メソッド・変数 | snake_case | `fetch_medias`, `media_id` |
| 定数 | UPPER_SNAKE_CASE | `_MEDIA_METRICS_FEED` |
| ファイル | snake_case | `instagram_repository.py` |
| モジュールレベル定数 | `_` プレフィックス（モジュールプライベート） | `_PHASE_INTERVALS` |

## テスト規約

- **TDD** で実装する（テストを先に書いてから実装）
- `make test` で全テストが通ること
- 外部 API（Instagram Graph API）は `MagicMock` でモックする
- データベースや CSV ファイルへの実アクセスはテストで行わない（`tmp_path` フィクスチャを使用）
- Singleton は `conftest.py` の `reset_singletons` フィクスチャでテスト間にリセットする
- テストクラスはテスト対象のメソッド・ケース単位でグループ化する

```python
class TestFetchMedias:
    def test_returns_list_of_instagram_media(self, ...):
        ...
    def test_handles_paging(self, ...):
        ...
```

## パッケージ管理

Poetry で依存パッケージを管理する。

```bash
# 本番パッケージ追加
poetry add <package>

# 開発パッケージ追加
poetry add <package> --group dev

# パッケージ削除
poetry remove <package>

# requirements.txt 更新（コンテナ内で実行）
./tools/update-requirements.sh
```

`pyproject.toml` を編集後は `requirements.txt` / `requirements-dev.txt` も更新してコミットする。

## Git 規約

### コミットメッセージ形式

```
<Prefix>: <メッセージ>
```

| Prefix | 用途 |
|---|---|
| `add` | 新規ファイル・機能の追加 |
| `update` | 既存機能の変更・改善 |
| `delete` | ファイル・機能の削除 |
| `fix` | バグ修正 |

### ブランチ戦略

[Gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) に準拠する。

![gitflow](./images/git-flow.png)

| ブランチ | 用途 |
|---|---|
| `main` | 本番リリース済みコード |
| `develop` | 開発統合ブランチ |
| `feature/<issue>-<title>` | 機能開発 |
| `release/<version>` | リリース準備 |
| `hotfix/<issue>-<title>` | 緊急バグ修正 |

## 開発プロセス

新機能追加・修正時は必ず以下の順序でドキュメントを作成してから実装を開始する。

1. `.steering/YYYYMMDD-<title>/requirements.md` を作成し、承認を得る
2. `.steering/YYYYMMDD-<title>/design.md` を作成し、承認を得る
3. `.steering/YYYYMMDD-<title>/tasklist.md` を作成し、承認を得る
4. tasklist に従って実装する
5. `make test` で動作確認する
