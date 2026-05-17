"""tests.test_instagram_service"""
import csv
import os
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch
import pytest

from models.instagram_media import InstagramMedia
from models.instagram_account import InstagramAccount
from services.instagram_service import InstagramService


def _make_media(media_id="m1", minutes_ago=30, media_product_type="FEED"):
    ts = (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).isoformat()
    return InstagramMedia.from_dict({
        "id": media_id, "timestamp": ts, "caption": "#test",
        "media_type": "IMAGE", "media_product_type": media_product_type,
        "permalink": "https://ig.com/p/1/", "media_url": None,
        "thumbnail_url": None, "like_count": 5, "comments_count": 1,
        "is_comment_enabled": True, "hashtags": ["#test"],
        "reach": 100, "saved": 5, "shares": 3,
        "profile_visits": 8, "follows": 1, "total_interactions": 20,
        "fetched_at": ts,
    })


def _make_account():
    ts = datetime.now(timezone.utc).isoformat()
    return InstagramAccount.from_dict({
        "username": "user", "biography": "bio",
        "followers_count": 1000, "follows_count": 200, "media_count": 50,
        "reach": 3000, "profile_views": 400,
        "website_clicks": 30, "fetched_at": ts,
    })


@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.fetch_medias.return_value = [_make_media("m1", minutes_ago=30)]
    repo.fetch_account.return_value = _make_account()
    return repo


@pytest.fixture
def service(tmp_path, mock_repo):
    with patch("services.instagram_service.InstagramRepository", return_value=mock_repo):
        svc = InstagramService(data_dir=str(tmp_path))
    return svc, tmp_path


class TestRun:
    def test_creates_media_csv(self, service):
        svc, tmp_path = service
        svc.run()
        assert (tmp_path / "media.csv").exists()

    def test_creates_account_snapshots_csv(self, service):
        svc, tmp_path = service
        svc.run()
        assert (tmp_path / "account_snapshots.csv").exists()

    def test_creates_media_snapshots_csv(self, service):
        svc, tmp_path = service
        svc.run()
        assert (tmp_path / "media_snapshots.csv").exists()

    def test_stories_csv_not_created(self, service):
        svc, tmp_path = service
        svc.run()
        assert not (tmp_path / "stories.csv").exists()

    def test_media_snapshot_contains_correct_columns(self, service):
        svc, tmp_path = service
        svc.run()
        with open(tmp_path / "media_snapshots.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 1
        assert rows[0]["id"] == "m1"
        assert "like_count" in rows[0]
        assert "reach" in rows[0]

    def test_media_snapshots_appended_on_every_run(self, service):
        svc, tmp_path = service
        svc.run()
        svc.run()
        with open(tmp_path / "media_snapshots.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 2

    def test_account_snapshots_appended_on_every_run(self, service):
        svc, tmp_path = service
        svc.run()
        svc.run()
        with open(tmp_path / "account_snapshots.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 2

    def test_media_csv_overwritten_on_every_run(self, service):
        svc, tmp_path = service
        svc.run()
        svc.run()
        with open(tmp_path / "media.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 1
