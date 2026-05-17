# glossary.md — ユビキタス言語定義

## ドメイン用語

| 日本語 | 英語（コード上） | 定義 |
|---|---|---|
| 投稿 | Media | Instagram に公開した画像・動画・リールのコンテンツ |
| リール | Reels | `media_product_type = "REELS"` の動画投稿。FEED 投稿と取得できるインサイト指標が異なる |
| ストーリー | Story | 24時間で消えるコンテンツ。アクティブなもののみ取得可能 |
| インサイト | Insights | リーチ・保存数・シェア数などのエンゲージメント指標 |
| スナップショット | Snapshot | 特定の時点におけるインサイト指標の記録 |
| フェーズスナップショット | Phase Snapshot | 投稿の経過時間に応じた間引きロジックを経た上で記録されるスナップショット |
| アクセストークン | Access Token | Instagram Graph API 認証に使用するトークン。長期トークンで約60日有効 |
| フォロワー数 | followers_count | アカウントをフォローしているユーザー数 |
| リーチ | reach | コンテンツを1回以上見たユニークアカウント数 |
| インプレッション | impressions | コンテンツが表示された合計回数（v22.0以降廃止） |

## フェーズ判定用語

| 用語 | 定義 |
|---|---|
| 投稿経過時間（post_age） | 投稿日時（`timestamp`）から現在時刻までの経過時間 |
| 最終取得日時（last_fetched） | `media_snapshots.csv` に記録された直近の `fetched_at` |
| 取得間隔（interval） | フェーズに応じたスナップショット取得の最小間隔 |

## API 用語

| 用語 | 定義 |
|---|---|
| Graph API | Meta（Facebook）が提供する Instagram のデータ取得 API |
| User ID | Instagram ビジネスアカウントの数値 ID（`config.ini` に設定） |
| ページング | 大量データを複数回のリクエストに分けて取得する仕組み。カーソルベース |
| total_value 形式 | アカウントインサイトの一部で使用されるレスポンス形式。`metric_type=total_value` で取得 |
| FEED | `media_product_type = "FEED"` の通常投稿（画像・動画） |
| REELS | `media_product_type = "REELS"` のリール投稿 |

## レイヤー用語

| 用語 | 定義 |
|---|---|
| Controller | エントリポイント。Service を呼び出し、例外をログに記録する |
| Service | フロー制御・ビジネスロジックを担うレイヤー |
| Repository | API 呼び出しとモデル変換を担うレイヤー |
| Accessor | 外部 API / ストレージへの低レベルアクセスを担うクラス |
| Model | データを表現する dataclass（`InstagramMedia` 等） |
| Singleton | アプリケーション内で1つのインスタンスのみ生成されるクラス（`Config`, `InstagramAccessor`） |

## CSV ファイル用語

| ファイル名 | 用語 | 定義 |
|---|---|---|
| `media.csv` | メディア一覧 | 実行時点の全投稿データ（毎回上書き） |
| `media_snapshots.csv` | メディアスナップショット | フェーズ判定を通過した時系列の指標記録（追記） |
| `stories.csv` | ストーリー一覧 | 実行時点のアクティブなストーリーズ（毎回上書き） |
| `account_snapshots.csv` | アカウントスナップショット | 毎実行時のアカウント指標記録（追記） |
