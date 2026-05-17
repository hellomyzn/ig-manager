"""tests.test_instagram_account"""
import json
from models.instagram_account import InstagramAccount


def _base_dict(**kwargs):
    base = {
        "username": "testuser",
        "biography": "Hello world",
        "followers_count": 1000,
        "follows_count": 200,
        "media_count": 50,
        "reach": 3000,
        "profile_views": 400,
        "website_clicks": 30,
        "fetched_at": "2026-05-17T21:05:00+0900",
    }
    base.update(kwargs)
    return base


class TestFromDict:
    def test_creates_model(self):
        acc = InstagramAccount.from_dict(_base_dict())
        assert acc.username == "testuser"
        assert acc.followers_count == 1000

    def test_optional_fields_can_be_none(self):
        acc = InstagramAccount.from_dict(_base_dict(biography=None, reach=None))
        assert acc.biography is None
        assert acc.reach is None


class TestToDict:
    def test_returns_all_fields(self):
        d = InstagramAccount.from_dict(_base_dict()).to_dict()
        assert d["followers_count"] == 1000
        assert d["profile_views"] == 400

    def test_without_none_field(self):
        d = InstagramAccount.from_dict(_base_dict(website_clicks=None)).to_dict(without_none_field=True)
        assert "website_clicks" not in d

    def test_biography_newlines_replaced_with_literal(self):
        d = InstagramAccount.from_dict(_base_dict(biography="line1\nline2\nline3")).to_dict()
        assert d["biography"] == "line1\\nline2\\nline3"

    def test_biography_none_remains_none(self):
        d = InstagramAccount.from_dict(_base_dict(biography=None)).to_dict()
        assert d["biography"] is None


class TestToJson:
    def test_valid_json(self):
        parsed = json.loads(InstagramAccount.from_dict(_base_dict()).to_json())
        assert parsed["username"] == "testuser"
