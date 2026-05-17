# Requirements: CSV日次蓄積 & GitHub Actions自動コミット

## 背景

現状の instagram_service.py は高頻度ポーリング（15分〜週1）を前提とした設計になっており、
毎日1回だけ実行するGitHub Actions運用には複雑すぎる。
また media.csv / stories.csv は上書き方式のため過去データが失われる。

## 変更内容

### 1. CSVの保存方針を簡素化（案A）

**廃止するファイル：**
- `stories.csv` — ストーリーデータの取得・保存は今回対象外

**変更するファイル：**
- `media.csv` — 現状維持（最新投稿一覧の上書き、マスターリスト用途）
- `media_snapshots.csv` — 毎実行時に全投稿のエンゲージメント指標を**無条件で追記**（フェーズ別インターバルロジックを廃止）
- `account_snapshots.csv` — 現状維持（毎実行時に追記）

**廃止するロジック：**
- `_PHASE_INTERVALS`（投稿年齢ごとに取得間隔を変える仕組み）
- `_should_snapshot()`（インターバル判定メソッド）
- `read_last_fetched()`（最終取得日時読み込み、不要になる）

### 2. GitHub Actions ワークフロー追加

**ファイル：** `.github/workflows/daily-fetch.yml`

**実行タイミング：** 毎日 9:00 JST（= UTC 00:00）

**処理内容：**
1. リポジトリをチェックアウト
2. Python 3.11 セットアップ
3. 依存ライブラリインストール（`src/requirements.txt`）
4. GitHub Secrets から `config.ini` を生成
5. `python src/main.py` を実行してデータ取得
6. `data/` 以下の CSV ファイルを自動コミット＆プッシュ

**必要な GitHub Secrets：**
- `INSTAGRAM_ACCESS_TOKEN`
- `INSTAGRAM_USER_ID`
- `INSTAGRAM_FACEBOOK_USER_ID`

## 受け入れ条件

- [ ] 毎日実行しても `media_snapshots.csv` と `account_snapshots.csv` に行が追記されること
- [ ] `media.csv` は最新の投稿一覧に上書きされること
- [ ] ストーリーデータは取得・保存されないこと
- [ ] GitHub Actionsが毎日9時JST（UTC 00:00）にトリガーされること
- [ ] データ取得後、CSVファイルが自動コミット＆プッシュされること
- [ ] Secretsが設定されていない場合はワークフローが失敗すること（意図通りのエラー）

## 制約

- ストーリーは今回スコープ外（将来追加可能な構造にする）
- Docker は使わず Python を直接 GitHub Actions 環境で実行する
- `config.ini` はリポジトリに含めない（Secrets経由で生成）
