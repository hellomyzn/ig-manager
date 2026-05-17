"""tests.test_instagram_service"""
import csv
import os
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch
import pytest

from models.instagram_media import InstagramMedia
from models.instagram_story import InstagramStory
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
        "reach": 100, "impressions": 200, "saved": 5, "shares": 3,
        "profile_visits": 8, "follows": 1, "total_interactions": 20,
        "plays": None, "video_views": None, "fetched_at": ts,
    })


def _make_story():
    ts = datetime.now(timezone.utc).isoformat()
    return InstagramStory.from_dict({
        "id": "s1", "timestamp": ts, "media_url": None, "permalink": None,
        "reach": 50, "impressions": 80, "replies": 2,
        "taps_forward": 10, "taps_back": 3, "exits": 1, "fetched_at": ts,
    })


def _make_account():
    ts = datetime.now(timezone.utc).isoformat()
    return InstagramAccount.from_dict({
        "username": "user", "biography": "bio",
        "followers_count": 1000, "follows_count": 200, "media_count": 50,
        "impressions": 5000, "reach": 3000, "profile_views": 400,
        "website_clicks": 30, "fetched_at": ts,
    })


@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.fetch_medias.return_value = [_make_media("m1", minutes_ago=30)]
    repo.fetch_stories.return_value = [_make_story()]
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

    def test_creates_stories_csv(self, service):
        svc, tmp_path = service
        svc.run()
        assert (tmp_path / "stories.csv").exists()

    def test_creates_account_snapshots_csv(self, service):
        svc, tmp_path = service
        svc.run()
        assert (tmp_path / "account_snapshots.csv").exists()

    def test_appends_media_snapshot_for_new_post(self, service):
        svc, tmp_path = service
        svc.run()
        snap_path = tmp_path / "media_snapshots.csv"
        assert snap_path.exists()
        with open(snap_path) as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 1
        assert rows[0]["id"] == "m1"

    def test_account_snapshots_appends_on_second_run(self, service):
        svc, tmp_path = service
        svc.run()
        svc.run()
        with open(tmp_path / "account_snapshots.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 2


class TestPhaseLogic:
    def test_snapshot_skipped_when_too_recent(self, tmp_path, mock_repo):
        """前回取得から間隔が短い場合はスナップショットを追記しない。"""
        recent_ts = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
        snap_path = tmp_path / "media_snapshots.csv"
        with open(snap_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "fetched_at"])
            writer.writeheader()
            writer.writerow({"id": "m1", "fetched_at": recent_ts})

        mock_repo.fetch_medias.return_value = [_make_media("m1", minutes_ago=30)]
        with patch("services.instagram_service.InstagramRepository", return_value=mock_repo):
            svc = InstagramService(data_dir=str(tmp_path))
        svc.run()

        with open(snap_path) as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 1

    def test_snapshot_taken_when_interval_elapsed(self, tmp_path, mock_repo):
        """前回取得から十分な時間が経過していればスナップショットを追記する。"""
        old_ts = (datetime.now(timezone.utc) - timedelta(minutes=20)).isoformat()
        snap_path = tmp_path / "media_snapshots.csv"
        with open(snap_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "fetched_at"])
            writer.writeheader()
            writer.writerow({"id": "m1", "fetched_at": old_ts})

        mock_repo.fetch_medias.return_value = [_make_media("m1", minutes_ago=30)]
        with patch("services.instagram_service.InstagramRepository", return_value=mock_repo):
            svc = InstagramService(data_dir=str(tmp_path))
        svc.run()

        with open(snap_path) as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 2
