"""models.instagram_account"""
import json
from dataclasses import dataclass
from typing import Optional

from models.model import Model, TModel


@dataclass
class InstagramAccount(Model):
    username: str
    biography: Optional[str]
    followers_count: int
    follows_count: int
    media_count: int
    impressions: Optional[int]
    reach: Optional[int]
    profile_views: Optional[int]
    website_clicks: Optional[int]
    fetched_at: str

    @classmethod
    def from_dict(cls: TModel, dict_: dict) -> TModel:
        return cls(
            username=dict_["username"],
            biography=dict_.get("biography"),
            followers_count=int(dict_["followers_count"]),
            follows_count=int(dict_["follows_count"]),
            media_count=int(dict_["media_count"]),
            impressions=_int_or_none(dict_.get("impressions")),
            reach=_int_or_none(dict_.get("reach")),
            profile_views=_int_or_none(dict_.get("profile_views")),
            website_clicks=_int_or_none(dict_.get("website_clicks")),
            fetched_at=dict_["fetched_at"],
        )

    def to_dict(self, without_none_field: bool = False) -> dict:
        d = {
            "username": self.username,
            "biography": self.biography,
            "followers_count": self.followers_count,
            "follows_count": self.follows_count,
            "media_count": self.media_count,
            "impressions": self.impressions,
            "reach": self.reach,
            "profile_views": self.profile_views,
            "website_clicks": self.website_clicks,
            "fetched_at": self.fetched_at,
        }
        if without_none_field:
            return {k: v for k, v in d.items() if v is not None}
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


def _int_or_none(val) -> Optional[int]:
    return int(val) if val is not None else None
