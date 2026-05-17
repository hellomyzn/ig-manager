"""tests.test_instagram_story"""
import json
import pytest
from models.instagram_story import InstagramStory


def _base_dict(**kwargs):
    base = {
        "id": "s1",
        "timestamp": "2026-05-17T20:00:00+0000",
        "media_url": "https://example.com/story.mp4",
        "permalink": "https://www.instagram.com/stories/user/s1/",
        "reach": 50,
        "replies": 2,
        "fetched_at": "2026-05-17T21:05:00+0900",
    }
    base.update(kwargs)
    return base


class TestFromDict:
    def test_creates_model(self):
        story = InstagramStory.from_dict(_base_dict())
        assert story.id == "s1"
        assert story.reach == 50

    def test_optional_fields_can_be_none(self):
        story = InstagramStory.from_dict(_base_dict(
            media_url=None, permalink=None, reach=None,
        ))
        assert story.media_url is None
        assert story.reach is None


class TestToDict:
    def test_returns_all_fields(self):
        d = InstagramStory.from_dict(_base_dict()).to_dict()
        assert d["id"] == "s1"
        assert d["reach"] == 50

    def test_without_none_field(self):
        d = InstagramStory.from_dict(_base_dict(replies=None)).to_dict(without_none_field=True)
        assert "replies" not in d


class TestToJson:
    def test_valid_json(self):
        parsed = json.loads(InstagramStory.from_dict(_base_dict()).to_json())
        assert parsed["id"] == "s1"
