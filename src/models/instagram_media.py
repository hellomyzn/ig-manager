"""models.instagram_media"""
import json
from dataclasses import dataclass
from typing import Optional

from models.model import Model, TModel


@dataclass
class InstagramMedia(Model):
    id: str
    timestamp: str
    caption: Optional[str]
    media_type: str
    media_product_type: str
    permalink: str
    media_url: Optional[str]
    thumbnail_url: Optional[str]
    like_count: int
    comments_count: int
    is_comment_enabled: bool
    hashtags: list
    reach: Optional[int]
    saved: Optional[int]
    shares: Optional[int]
    profile_visits: Optional[int]
    follows: Optional[int]
    total_interactions: Optional[int]
    fetched_at: str

    @property
    def is_reel(self) -> bool:
        return self.media_product_type == "REELS"

    @classmethod
    def from_dict(cls: TModel, dict_: dict) -> TModel:
        hashtags_raw = dict_.get("hashtags", [])
        if isinstance(hashtags_raw, str):
            hashtags = [h for h in hashtags_raw.split(",") if h]
        else:
            hashtags = list(hashtags_raw)
        return cls(
            id=dict_["id"],
            timestamp=dict_["timestamp"],
            caption=dict_.get("caption"),
            media_type=dict_["media_type"],
            media_product_type=dict_["media_product_type"],
            permalink=dict_["permalink"],
            media_url=dict_.get("media_url"),
            thumbnail_url=dict_.get("thumbnail_url"),
            like_count=int(dict_["like_count"]),
            comments_count=int(dict_["comments_count"]),
            is_comment_enabled=bool(dict_["is_comment_enabled"]),
            hashtags=hashtags,
            reach=_int_or_none(dict_.get("reach")),
            saved=_int_or_none(dict_.get("saved")),
            shares=_int_or_none(dict_.get("shares")),
            profile_visits=_int_or_none(dict_.get("profile_visits")),
            follows=_int_or_none(dict_.get("follows")),
            total_interactions=_int_or_none(dict_.get("total_interactions")),
            fetched_at=dict_["fetched_at"],
        )

    def to_dict(self, without_none_field: bool = False) -> dict:
        d = {
            "id": self.id,
            "timestamp": self.timestamp,
            "caption": self.caption.replace("\n", "\\n") if self.caption else self.caption,
            "media_type": self.media_type,
            "media_product_type": self.media_product_type,
            "permalink": self.permalink,
            "media_url": self.media_url,
            "thumbnail_url": self.thumbnail_url,
            "like_count": self.like_count,
            "comments_count": self.comments_count,
            "is_comment_enabled": self.is_comment_enabled,
            "hashtags": ",".join(self.hashtags),
            "reach": self.reach,
            "saved": self.saved,
            "shares": self.shares,
            "profile_visits": self.profile_visits,
            "follows": self.follows,
            "total_interactions": self.total_interactions,
            "fetched_at": self.fetched_at,
        }
        if without_none_field:
            return {k: v for k, v in d.items() if v is not None}
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


def _int_or_none(val) -> Optional[int]:
    return int(val) if val is not None else None
