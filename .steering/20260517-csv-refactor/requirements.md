# requirements.md — CSV カラム整理 & 出力先変更

## 概要

2点の変更を行う。

1. **CSV カラム整理** — Instagram Graph API で実際には取得できない（常に null の）フィールドをモデル・CSV から削除する
2. **CSV 出力先変更** — `src/data/` から `../../footprints/instagram`（プロジェクトルートから見た相対パス）に変更し、Docker の bind mount で参照・書き込みを行う

## カラム整理の対象

現在の実装で取得しているメトリクスを確認し、一度も API から値が返らないフィールドを削除する。

### InstagramMedia — 削除対象フィールド

| フィールド | 理由 |
|---|---|
| `impressions` | v22.0 で廃止。メトリクス定数から除外済みのため常に null |
| `plays` | v22.0 で廃止。メトリクス定数から除外済みのため常に null |
| `video_views` | FEED・REELS いずれのメトリクス定数にも含まれていないため常に null |

### InstagramStory — 削除対象フィールド

| フィールド | 理由 |
|---|---|
| `impressions` | v25.0 で廃止。メトリクス定数から除外済みのため常に null |
| `taps_forward` | v25.0 で廃止。メトリクス定数から除外済みのため常に null |
| `taps_back` | v25.0 で廃止。メトリクス定数から除外済みのため常に null |
| `exits` | v25.0 で廃止。メトリクス定数から除外済みのため常に null |

### InstagramAccount — 削除対象フィールド

| フィールド | 理由 |
|---|---|
| `impressions` | v25.0 で廃止。メトリクス定数から除外済みのため常に null |

## CSV 出力先変更

| 項目 | 変更前 | 変更後 |
|---|---|---|
| ホストパス | `./src/data/` | `../../footprints/instagram` |
| コンテナパス | `/opt/work/data/` | `/opt/footprints/instagram` |
| 管理方法 | gitignore のみ | Docker bind mount で永続化 |

`../../footprints/instagram` は `ig-manager` プロジェクトルートからの相対パスであり、ホストの絶対パスは `/Users/myzn/projects/footprints/instagram` に相当する。

## 既存 CSV データ

現在の `src/data/*.csv` は削除してよい。

## 受け入れ条件

- [ ] 削除対象フィールドがモデル・テスト・CSV から除去されていること
- [ ] `make test` が通ること
- [ ] `make run` で `/opt/footprints/instagram/` 配下に CSV が生成されること
- [ ] ホスト側 `../../footprints/instagram/` に CSV が反映されること
