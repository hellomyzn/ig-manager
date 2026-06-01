# Requirements: データ管理を footprints リポジトリへ移行

## 背景

現在、Instagram のデータ（CSV ファイル）が ig-manager リポジトリの `data/` ディレクトリに保存され、GitHub にも毎日コミットされている。
データは ig-manager のコードとは無関係であり、別リポジトリ（footprints）で管理すべき。

## 目的

- ig-manager リポジトリからデータを完全に切り離す
- データは `../../footprints/instagram/` で一元管理する
- ig-manager の git 履歴からも `data/` を除去する
- footprints リポジトリにデータの git 履歴（daily fetch コミット群）を移行する

## 変更内容

### 1. git 履歴の移行（ig-manager → footprints）

- ig-manager の `data/` ディレクトリの 15 コミット履歴（2026-05-18 〜 2026-06-01）を footprints に移行
- `data/` → `instagram/` にパスをリネームして取り込む
- footprints 側の既存 instagram コミット（2026-05-17 の 4 コミット）を親として、ig-manager の履歴を graft（接ぎ木）し、線形履歴を構成する

### 2. ig-manager リポジトリの変更

- `data/` を `.gitignore` に追加
- `git filter-repo` で `data/` を履歴ごと削除
- GitHub へ force push

### 3. GitHub Actions の変更

- 現在: ig-manager の `data/` に書き込み → ig-manager リポジトリにコミット・push
- 変更後: footprints リポジトリの `instagram/` に書き込み → footprints リポジトリにコミット・push
- footprints リポジトリへの push に PAT（Personal Access Token）が必要なため、ig-manager の GitHub Secrets に `FOOTPRINTS_PAT` を追加する

## 受け入れ条件

- [ ] ig-manager の git 履歴に `data/` が含まれていない
- [ ] ig-manager の GitHub リポジトリに `data/` が存在しない
- [ ] footprints の `instagram/` に 15 コミット分の daily fetch 履歴が含まれている
- [ ] footprints の `instagram/` 履歴が May 17 → May 18〜 と時系列で線形に繋がっている
- [ ] GitHub Actions が毎日 footprints リポジトリに正しく push できる
- [ ] ローカル開発環境（Docker）は引き続き `../../footprints/instagram` を参照できる

## 制約事項

- ig-manager / footprints 両リポジトリへの force push が発生する
- GitHub Actions に `FOOTPRINTS_PAT` シークレットの手動追加が必要
- ローカルの `data/` ディレクトリは gitignore 後もファイルとして残る（Docker mount 用）
