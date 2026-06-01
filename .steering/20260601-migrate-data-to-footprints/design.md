# Design: データ管理を footprints リポジトリへ移行

## 実装アプローチ

### フェーズ1: git 履歴の移行

#### 1-1. ig-manager の data/ 履歴を抽出

ig-manager を一時ディレクトリにクローンし、`git filter-repo` で `data/` のみを残しつつ `instagram/` にリネームする。

```bash
# 一時クローン
git clone /Users/myzn/projects/python/ig-manager /tmp/ig-data-extract
cd /tmp/ig-data-extract

# data/ のみ残して instagram/ にリネーム
git filter-repo --path data/ --path-rename data/:instagram/
```

結果: `/tmp/ig-data-extract` に 15コミットのみの履歴が残る（全て `instagram/` パス）

#### 1-2. graft で footprints の履歴に接続

footprints の最後の instagram コミット（`199b9c49`）を、抽出した履歴の最初のコミットの親として設定する。

```
footprints 既存履歴:
  b95eb3af → ac4413db → 241801eb → 199b9c49 (update: isntagram, May 17)

ig-manager 抽出履歴:
  [root] e8eb921 (daily fetch 2026-05-18) → ... → 4807037 (daily fetch 2026-06-01)

graft 後:
  ... → 199b9c49 → e8eb921 → ... → 4807037
```

実装手順:
```bash
cd /tmp/ig-data-extract

# 抽出履歴の最初のコミット（root）を確認
ROOT=$(git log --oneline | tail -1 | awk '{print $1}')

# footprints の対象コミットハッシュ（199b9c49）を親として graft
echo "$ROOT $(cd /Users/myzn/projects/footprints && git rev-parse 199b9c49)" >> .git/info/grafts

# graft を永続化（filter-repo で書き換え）
git filter-repo --force
```

#### 1-3. footprints に取り込む

```bash
cd /Users/myzn/projects/footprints

# 抽出リポジトリを remote として追加
git remote add ig-extract /tmp/ig-data-extract
git fetch ig-extract

# fast-forward で取り込み（graft により線形になっているため）
# ig-extract/main が footprints/main の先にある instagram コミットを含む
git rebase --onto ig-extract/main $(git merge-base HEAD ig-extract/main) HEAD
# または merge
git merge ig-extract/main --allow-unrelated-histories

# remote を削除
git remote remove ig-extract
```

> **注意**: graft による接続後、footprints の instagram/ ファイルと抽出履歴の instagram/ ファイルが競合する可能性がある。その場合は ig-manager 側（最新データ）を優先して解決する。

---

### フェーズ2: ig-manager の変更

#### 2-1. .gitignore に data/ を追加

```
# Data (managed in footprints repository)
data/
```

#### 2-2. ig-manager の git 履歴から data/ を削除

```bash
cd /Users/myzn/projects/python/ig-manager
git filter-repo --path data/ --invert-paths
```

#### 2-3. GitHub へ force push

```bash
git push origin main --force
```

---

### フェーズ3: GitHub Actions の変更

#### 変更前

```yaml
- name: Fetch Instagram data
  run: |
    mkdir -p data src/logs
    cd src && DATA_DIR=../data PYTHONPATH=. python main.py

- name: Commit and push CSV files
  run: |
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
    git add data/
    git diff --staged --quiet && echo "No changes to commit" || (
      git commit -m "data: daily fetch $(date -u '+%Y-%m-%d')" &&
      git push
    )
```

#### 変更後

```yaml
- name: Checkout footprints repository
  uses: actions/checkout@v4
  with:
    repository: hellomyzn/footprints
    path: footprints
    token: ${{ secrets.FOOTPRINTS_PAT }}

- name: Fetch Instagram data
  run: |
    mkdir -p footprints/instagram src/logs
    cd src && DATA_DIR=../footprints/instagram PYTHONPATH=. python main.py

- name: Commit and push to footprints
  working-directory: footprints
  run: |
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
    git add instagram/
    git diff --staged --quiet && echo "No changes to commit" || (
      git commit -m "data: daily fetch $(date -u '+%Y-%m-%d')" &&
      git push
    )
```

#### 必要なシークレット追加

| シークレット名 | 内容 | 設定場所 |
|---|---|---|
| `FOOTPRINTS_PAT` | footprints リポジトリへの write 権限を持つ PAT | ig-manager の GitHub Secrets |

PAT の必要スコープ: `repo`（または `contents: write` の Fine-grained token）

---

## 変更するコンポーネント

| ファイル | 変更内容 |
|---|---|
| `.gitignore` | `data/` を追加 |
| `.github/workflows/daily-fetch.yml` | footprints リポジトリへ push するよう変更 |
| ig-manager git 履歴 | `data/` を filter-repo で削除 |
| footprints git 履歴 | ig-manager の 15コミットを graft で取り込み |

## 影響範囲

- **ローカル開発（Docker）**: 変更不要。docker-compose.yml はすでに `../../footprints/instagram` をマウント済み
- **ig-manager のコード（src/）**: 変更不要。`DATA_DIR` 環境変数で制御されており、Docker 経由では `/opt/footprints/instagram` を参照
- **GitHub Actions**: ワークフローファイルの変更 + PAT シークレットの追加が必要

## リスクと対策

| リスク | 対策 |
|---|---|
| graft 後の競合 | ig-manager 側（最新）を優先して手動解決 |
| force push による他者への影響 | 個人リポジトリのため影響なし |
| PAT の権限不足 | Fine-grained token で `contents: write` を明示的に付与 |
