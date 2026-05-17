# Tasklist: CSV改行問題の修正

## タスク一覧

- [x] `src/models/instagram_account.py` の `to_dict()` で `biography` の改行を `\n` リテラルに置換
- [x] `src/models/instagram_media.py` の `to_dict()` で `caption` の改行を `\n` リテラルに置換
- [x] 既存の `account_snapshots.csv` を修正（47件）
- [x] 既存の `media.csv` を修正（47件）
- [x] テストの確認・更新（改行を含む `biography` / `caption` のテストケースを追加）

## 完了条件

- CSVの各レコードが1行で出力される
- テストがすべてパスする
