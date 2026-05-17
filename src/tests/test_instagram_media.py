"""tests.test_instagram_media"""
import json
import pytest
from models.instagram_media import InstagramMedia


def _base_dict(**kwargs):
    base = {
        "id": "123",
        "timestamp": "2026-05-17T21:00:00+0000",
        "caption": "#test #photo today",
        "media_type": "IMAGE",
        "media_product_type": "FEED",
        "permalink": "https://www.instagram.com/p/abc/",
        "media_url": "https://example.com/img.jpg",
        "thumbnail_url": None,
        "like_count": 10,
        "comments_count": 2,
        "is_comment_enabled": True,
        "hashtags": ["#test", "#photo"],
        "reach": 100,
        "impressions": 200,
        "saved": 5,
        "shares": 3,
        "profile_visits": 8,
        "follows": 1,
        "total_interactions": 21,
        "plays": None,
        "video_views": None,
        "fetched_at": "2026-05-17T21:05:00+0900",
    }
    base.update(kwargs)
    return base


class TestFromDict:
    def test_creates_model_from_full_dict(self):
        media = InstagramMedia.from_dict(_base_dict())
        assert media.id == "123"
        assert media.like_count == 10
        assert media.hashtags == ["#test", "#photo"]

    def test_optional_fields_can_be_none(self):
        media = InstagramMedia.from_dict(_base_dict(
            caption=None,
            media_url=None,
            thumbnail_url=None,
            reach=None,
            plays=None,
        ))
        assert media.caption is None
        assert media.reach is None

    def test_hashtags_stored_as_list(self):
        media = InstagramMedia.from_dict(_base_dict(hashtags=["#a", "#b", "#c"]))
        assert media.hashtags == ["#a", "#b", "#c"]

    def test_is_reel_returns_true_for_reels(self):
        media = InstagramMedia.from_dict(_base_dict(media_product_type="REELS"))
        assert media.is_reel is True

    def test_is_reel_returns_false_for_feed(self):
        media = InstagramMedia.from_dict(_base_dict(media_product_type="FEED"))
        assert media.is_reel is False


class TestToDict:
    def test_to_dict_returns_all_fields(self):
        media = InstagramMedia.from_dict(_base_dict())
        d = media.to_dict()
        assert d["id"] == "123"
        assert d["like_count"] == 10
        assert d["hashtags"] == "#test,#photo"

    def test_to_dict_without_none_field(self):
        media = InstagramMedia.from_dict(_base_dict(plays=None, video_views=None))
        d = media.to_dict(without_none_field=True)
        assert "plays" not in d
        assert "video_views" not in d

    def test_to_dict_hashtags_as_csv_string(self):
        media = InstagramMedia.from_dict(_base_dict(hashtags=["#x", "#y"]))
        assert media.to_dict()["hashtags"] == "#x,#y"

    def test_to_dict_empty_hashtags(self):
        media = InstagramMedia.from_dict(_base_dict(hashtags=[]))
        assert media.to_dict()["hashtags"] == ""


class TestToJson:
    def test_to_json_is_valid_json(self):
        media = InstagramMedia.from_dict(_base_dict())
        parsed = json.loads(media.to_json())
        assert parsed["id"] == "123"
