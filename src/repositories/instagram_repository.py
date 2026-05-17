"""repositories.instagram_repository"""
import re
from dataclasses import dataclass
from datetime import datetime, timezone

from common.instagram import InstagramAccessor
from common.log import warn
from models.instagram_media import InstagramMedia
from models.instagram_story import InstagramStory
from models.instagram_account import InstagramAccount

_MEDIA_FIELDS = (
    "id,timestamp,caption,media_type,media_product_type,"
    "permalink,media_url,thumbnail_url,like_count,comments_count,is_comment_enabled"
)
_MEDIA_METRICS_FEED = "reach,saved,shares,profile_visits,follows,total_interactions"
_MEDIA_METRICS_REELS = "reach,saved,shares,total_interactions"
_STORY_FIELDS = "id,timestamp,media_url,permalink"
_STORY_METRICS = "reach,replies"
_ACCOUNT_FIELDS = "username,biography,followers_count,follows_count,media_count"
_ACCOUNT_METRICS_TIMESERIES = "reach"
_ACCOUNT_METRICS_TOTAL = "profile_views,website_clicks"


@dataclass
class InstagramRepository:
    """Instagram Graph API からデータを取得してモデルに変換する。"""

    def __post_init__(self):
        self._accessor = InstagramAccessor()

    def fetch_medias(self) -> list:
        """全投稿を取得する（ページング対応）。"""
        items = self._fetch_all_media_items()
        fetched_at = _now_iso()
        result = []
        for item in items:
            insights = self._fetch_media_insights(item["id"], item.get("media_product_type", ""))
            media = InstagramMedia.from_dict({
                **item,
                "hashtags": _extract_hashtags(item.get("caption") or ""),
                "fetched_at": fetched_at,
                **insights,
            })
            result.append(media)
        return result

    def fetch_stories(self) -> list:
        """アクティブなストーリーズを取得する。"""
        response = self._accessor.get(
            f"{self._accessor.user_id}/stories",
            {"fields": _STORY_FIELDS},
        )
        fetched_at = _now_iso()
        result = []
        for item in response.get("data", []):
            insights = self._fetch_story_insights(item["id"])
            story = InstagramStory.from_dict({**item, "fetched_at": fetched_at, **insights})
            result.append(story)
        return result

    def fetch_account(self) -> InstagramAccount:
        """アカウント基本情報と日次インサイトを取得する。"""
        fetched_at = _now_iso()
        profile = self._accessor.get(
            self._accessor.user_id,
            {"fields": _ACCOUNT_FIELDS},
        )
        insights = self._fetch_account_insights()
        return InstagramAccount.from_dict({**profile, "fetched_at": fetched_at, **insights})

    def _fetch_account_insights(self) -> dict:
        result = {}
        try:
            resp = self._accessor.get(
                f"{self._accessor.user_id}/insights",
                {"metric": _ACCOUNT_METRICS_TIMESERIES, "period": "day"},
            )
            result.update(self._accessor.parse_insights(resp))
        except Exception as e:
            warn("Failed to fetch account time-series insights: {0}", e)
        try:
            resp = self._accessor.get(
                f"{self._accessor.user_id}/insights",
                {"metric": _ACCOUNT_METRICS_TOTAL, "metric_type": "total_value", "period": "day"},
            )
            result.update(self._accessor.parse_total_value_insights(resp))
        except Exception as e:
            warn("Failed to fetch account total_value insights: {0}", e)
        return result

    def _fetch_all_media_items(self) -> list:
        items = []
        params = {"fields": _MEDIA_FIELDS}
        while True:
            response = self._accessor.get(f"{self._accessor.user_id}/media", params)
            items.extend(response.get("data", []))
            next_cursor = response.get("paging", {}).get("cursors", {}).get("after")
            if not next_cursor or "next" not in response.get("paging", {}):
                break
            params = {"fields": _MEDIA_FIELDS, "after": next_cursor}
        return items

    def _fetch_media_insights(self, media_id: str, media_product_type: str) -> dict:
        metrics = _MEDIA_METRICS_REELS if media_product_type == "REELS" else _MEDIA_METRICS_FEED
        try:
            response = self._accessor.get(f"{media_id}/insights", {"metric": metrics})
            return self._accessor.parse_insights(response)
        except Exception as e:
            warn("Failed to fetch insights for media {0}: {1}", media_id, e)
            return {}

    def _fetch_story_insights(self, story_id: str) -> dict:
        try:
            response = self._accessor.get(f"{story_id}/insights", {"metric": _STORY_METRICS})
            return self._accessor.parse_insights(response)
        except Exception as e:
            warn("Failed to fetch insights for story {0}: {1}", story_id, e)
            return {}


def _extract_hashtags(caption: str) -> list:
    return re.findall(r"#\w+", caption)


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()
