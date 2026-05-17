"""models.instagram_story"""
import json
from dataclasses import dataclass
from typing import Optional

from models.model import Model, TModel


@dataclass
class InstagramStory(Model):
    id: str
    timestamp: str
    media_url: Optional[str]
    permalink: Optional[str]
    reach: Optional[int]
    replies: Optional[int]
    fetched_at: str

    @classmethod
    def from_dict(cls: TModel, dict_: dict) -> TModel:
        return cls(
            id=dict_["id"],
            timestamp=dict_["timestamp"],
            media_url=dict_.get("media_url"),
            permalink=dict_.get("permalink"),
            reach=_int_or_none(dict_.get("reach")),
            replies=_int_or_none(dict_.get("replies")),
            fetched_at=dict_["fetched_at"],
        )

    def to_dict(self, without_none_field: bool = False) -> dict:
        d = {
            "id": self.id,
            "timestamp": self.timestamp,
            "media_url": self.media_url,
            "permalink": self.permalink,
            "reach": self.reach,
            "replies": self.replies,
            "fetched_at": self.fetched_at,
        }
        if without_none_field:
            return {k: v for k, v in d.items() if v is not None}
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


def _int_or_none(val) -> Optional[int]:
    return int(val) if val is not None else None
