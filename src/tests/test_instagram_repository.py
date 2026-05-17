"""tests.test_instagram_repository"""
from unittest.mock import MagicMock, patch
import pytest
from repositories.instagram_repository import InstagramRepository


@pytest.fixture
def mock_accessor():
    accessor = MagicMock()
    accessor.user_id = "uid"
    return accessor


@pytest.fixture
def repo(mock_accessor):
    with patch("repositories.instagram_repository.InstagramAccessor", return_value=mock_accessor):
        return InstagramRepository()


def _media_item(media_id="m1", media_product_type="FEED"):
    return {
        "id": media_id,
        "timestamp": "2026-05-17T21:00:00+0000",
        "caption": "#hello #world",
        "media_type": "IMAGE",
        "media_product_type": media_product_type,
        "permalink": "https://www.instagram.com/p/abc/",
        "media_url": "https://example.com/img.jpg",
        "thumbnail_url": None,
        "like_count": 5,
        "comments_count": 1,
        "is_comment_enabled": True,
    }


def _insight_response(*metrics):
    return {
        "data": [{"name": m, "values": [{"value": 10}]} for m in metrics]
    }


class TestFetchMedias:
    def test_returns_list_of_instagram_media(self, repo, mock_accessor):
        mock_accessor.get.side_effect = [
            {"data": [_media_item("m1")], "paging": {}},
            _insight_response("reach", "impressions", "saved", "shares",
                              "profile_visits", "follows", "total_interactions"),
        ]
        mock_accessor.parse_insights.return_value = {"reach": 10, "impressions": 20}
        result = repo.fetch_medias()
        assert len(result) == 1
        assert result[0].id == "m1"

    def test_extracts_hashtags_from_caption(self, repo, mock_accessor):
        mock_accessor.get.side_effect = [
            {"data": [_media_item("m1")], "paging": {}},
            _insight_response("reach"),
        ]
        mock_accessor.parse_insights.return_value = {}
        result = repo.fetch_medias()
        assert "#hello" in result[0].hashtags
        assert "#world" in result[0].hashtags

    def test_handles_paging(self, repo, mock_accessor):
        mock_accessor.get.side_effect = [
            # 全ページ取得（paging loop）
            {"data": [_media_item("m1")], "paging": {"cursors": {"after": "cursor1"}, "next": "url"}},
            {"data": [_media_item("m2")], "paging": {}},
            # 各投稿のインサイト取得
            _insight_response("reach"),
            _insight_response("reach"),
        ]
        mock_accessor.parse_insights.return_value = {}
        result = repo.fetch_medias()
        assert len(result) == 2

    def test_reel_uses_reels_metrics(self, repo, mock_accessor):
        mock_accessor.get.side_effect = [
            {"data": [_media_item("m1", media_product_type="REELS")], "paging": {}},
            _insight_response("reach", "saved", "shares", "total_interactions"),
        ]
        mock_accessor.parse_insights.return_value = {"reach": 5, "total_interactions": 10}
        result = repo.fetch_medias()
        assert result[0].reach == 5
        assert result[0].total_interactions == 10

    def test_skips_media_when_insight_fetch_fails(self, repo, mock_accessor):
        mock_accessor.get.side_effect = [
            {"data": [_media_item("m1")], "paging": {}},
            Exception("API error"),
        ]
        result = repo.fetch_medias()
        assert len(result) == 1
        assert result[0].reach is None


class TestFetchStories:
    def test_returns_list_of_instagram_story(self, repo, mock_accessor):
        mock_accessor.get.side_effect = [
            {"data": [{"id": "s1", "timestamp": "2026-05-17T20:00:00+0000",
                       "media_url": "https://ex.com/s.mp4", "permalink": "https://ig.com/s/1/"}]},
            _insight_response("reach", "impressions"),
        ]
        mock_accessor.parse_insights.return_value = {"reach": 50, "impressions": 80}
        result = repo.fetch_stories()
        assert len(result) == 1
        assert result[0].id == "s1"
        assert result[0].reach == 50

    def test_returns_empty_list_when_no_stories(self, repo, mock_accessor):
        mock_accessor.get.return_value = {"data": []}
        result = repo.fetch_stories()
        assert result == []


class TestFetchAccount:
    def test_returns_instagram_account(self, repo, mock_accessor):
        mock_accessor.get.side_effect = [
            {"username": "user", "biography": "bio", "followers_count": 1000,
             "follows_count": 200, "media_count": 50},
            {"data": [{"name": "reach", "values": [{"value": 3000}]}]},
            {"data": [{"name": "profile_views", "total_value": {"value": 400}}]},
        ]
        mock_accessor.parse_insights.return_value = {"reach": 3000}
        mock_accessor.parse_total_value_insights.return_value = {"profile_views": 400}
        result = repo.fetch_account()
        assert result.username == "user"
        assert result.followers_count == 1000
