# Tasklist: データ管理を footprints リポジトリへ移行

## タスク一覧

### フェーズ1: git 履歴の移行

- [ ] **1-1.** git filter-repo がインストールされているか確認（未インストールなら `pip install git-filter-repo`）
- [ ] **1-2.** ig-manager を `/tmp/ig-data-extract` に一時クローン
- [ ] **1-3.** 一時クローンで `git filter-repo --path data/ --path-rename data/:instagram/` を実行
- [ ] **1-4.** 抽出履歴の root コミットハッシュを確認
- [ ] **1-5.** graft ファイルを作成（root の親を footprints の `199b9c49` に設定）
- [ ] **1-6.** `git filter-repo --force` で graft を永続化
- [ ] **1-7.** footprints に `ig-extract` remote を追加して fetch
- [ ] **1-8.** footprints に merge（競合があれば ig-manager 側を優先して解決）
- [ ] **1-9.** `ig-extract` remote を削除
- [ ] **1-10.** footprints の履歴が線形になっていることを確認（`git log --oneline -- instagram/`）
- [ ] **1-11.** footprints を GitHub へ push

### フェーズ2: ig-manager のクリーンアップ

- [ ] **2-1.** `.gitignore` に `data/` を追加してコミット
- [ ] **2-2.** `git filter-repo --path data/ --invert-paths` で `data/` を履歴ごと削除
- [ ] **2-3.** ig-manager を GitHub へ force push
- [ ] **2-4.** GitHub 上の ig-manager に `data/` が存在しないことを確認

### フェーズ3: GitHub Actions の変更

- [ ] **3-1.** `FOOTPRINTS_PAT`（Fine-grained PAT、`contents: write`）を GitHub で発行
- [ ] **3-2.** ig-manager の GitHub Secrets に `FOOTPRINTS_PAT` を登録
- [ ] **3-3.** `.github/workflows/daily-fetch.yml` を変更（footprints checkout + instagram/ への書き込み）
- [ ] **3-4.** ワークフローを手動実行（`workflow_dispatch`）して動作確認
- [ ] **3-5.** footprints に新しい daily fetch コミットが追加されることを確認

## 完了条件

- ig-manager の git 履歴・GitHub に `data/` が存在しない
- footprints の `git log --oneline -- instagram/` に 19 コミット以上（既存 4 + 移行 15）が線形で表示される
- GitHub Actions の手動実行が成功し、footprints に新コミットが追加される
