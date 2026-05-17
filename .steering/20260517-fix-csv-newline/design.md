# Design: CSV改行問題の修正

## 実装アプローチ

モデルの `to_dict()` メソッド内で、CSV出力前に改行文字を `\n` リテラルに置換する。

CSV書き込み層ではなくモデル層で対応することで、`to_dict()` を経由するすべての出力（CSV・JSON）で一貫した形式となる。

## 変更するコンポーネント

### `src/models/instagram_account.py`

`to_dict()` の `biography` フィールドで置換処理を追加。

```python
"biography": self.biography.replace("\n", "\\n") if self.biography else self.biography,
```

### `src/models/instagram_media.py`

`to_dict()` の `caption` フィールドで置換処理を追加。

```python
"caption": self.caption.replace("\n", "\\n") if self.caption else self.caption,
```

## 既存CSVの修正

既存の `account_snapshots.csv` と `media.csv` に含まれる改行文字も同様にリテラル置換する。Pythonスクリプトで `csv.DictReader` / `csv.DictWriter` を使いインプレース修正する。

## 影響範囲の分析

- `to_dict()` は CSV書き込みと `to_json()` の両方から呼ばれる
- `from_dict()` でCSVを読み込む際、`\n` リテラルはそのまま文字列として扱われる（自動復元はされない）
- テスト側で `biography` / `caption` に改行を含むケースがあれば更新が必要
