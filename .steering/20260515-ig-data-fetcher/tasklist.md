# tasklist.md — Instagram データ取得機能

## タスク一覧

### 0. 事前準備
- [x] `src/data/` ディレクトリ作成
- [x] `.gitignore` に `src/data/` を追加
- [x] `src/common/config/config.template.ini` に `[INSTAGRAM]` セクション追加
- [x] `src/common/config/config.ini` に `[INSTAGRAM]` セクション追加（実値を設定）

### 1. common/instagram — API クライアント
- [x] `src/common/instagram/__init__.py` 作成
- [x] `src/common/instagram/instagram_accessor.py` 作成

### 2. common/csv — CSV 読み書き
- [x] `src/common/csv/__init__.py` 作成
- [x] `src/common/csv/csv_writer.py` 作成

### 3. models — データモデル
- [x] `src/models/instagram_media.py` 作成
- [x] `src/models/instagram_story.py` 作成
- [x] `src/models/instagram_account.py` 作成
- [x] `src/models/__init__.py` に各モデルを追加

### 4. repositories — API 呼び出し・モデル変換
- [x] `src/repositories/instagram_repository.py` 作成

### 5. services — フロー制御・フェーズ判定・CSV 書き出し
- [x] `src/services/instagram_service.py` 作成

### 6. controllers — エントリポイント
- [x] `src/controllers/instagram_controller.py` 作成

### 7. main.py 更新
- [x] `src/main.py` に `InstagramController().run()` 呼び出し追加

### 8. 動作確認
- [x] `data/media.csv` が生成されること（48KB）
- [x] `data/media_snapshots.csv` が追記されること
- [x] `data/stories.csv` が生成されること
- [x] `data/account_snapshots.csv` が追記されること
- [x] フェーズ判定が正しく動作すること

## 完了条件
- [x] 全タスクが完了
- [x] `make run` で4つの CSV が正しく生成・更新される
- [x] エラー時にリトライ・ログ出力が機能する

## v25.0 API 対応メモ（実装中に判明した制約）

| メトリクス | 状況 |
|---|---|
| `impressions`（メディア） | v22.0 で廃止 → null 保存 |
| `plays`（リール） | v22.0 で廃止 → null 保存 |
| `video_views`（リール） | REELS 種別では使用不可 → null 保存 |
| `profile_visits`, `follows`（リール） | REELS 種別では使用不可 → null 保存 |
| `impressions`（アカウント） | v25.0 で廃止 → null 保存 |
| `profile_views`, `website_clicks`（アカウント） | `metric_type=total_value&period=day` が必要 |
| `taps_forward`, `taps_back`, `exits`（ストーリー） | v25.0 で廃止 → null 保存 |
