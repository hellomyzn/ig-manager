"""services.instagram_service"""
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from common.csv import write, read_last_fetched
from common.log import info, warn
from repositories.instagram_repository import InstagramRepository

_DEFAULT_DATA_DIR = "data"

_PHASE_INTERVALS = [
    (timedelta(hours=1),  timedelta(minutes=15)),
    (timedelta(hours=24), timedelta(hours=1)),
    (timedelta(days=7),   timedelta(days=1)),
    (None,                timedelta(days=7)),
]

_SNAPSHOT_COLS = [
    "id", "fetched_at", "like_count", "comments_count",
    "reach", "impressions", "saved", "shares",
    "profile_visits", "follows", "total_interactions",
    "plays", "video_views",
]


@dataclass
class InstagramService:
    data_dir: str = _DEFAULT_DATA_DIR

    def __post_init__(self):
        os.makedirs(self.data_dir, exist_ok=True)
        self._repo = InstagramRepository()

    def run(self) -> None:
        """全データを取得して CSV に書き出す。"""
        info("Instagram data fetch started")

        medias = self._repo.fetch_medias()
        stories = self._repo.fetch_stories()
        account = self._repo.fetch_account()

        self._write_medias(medias)
        self._write_stories(stories)
        self._write_account(account)

        info("Instagram data fetch completed")

    def _write_medias(self, medias: list) -> None:
        media_path = os.path.join(self.data_dir, "media.csv")
        snap_path = os.path.join(self.data_dir, "media_snapshots.csv")

        last_fetched = read_last_fetched(snap_path, id_col="id")
        now = datetime.now(timezone.utc)

        write(media_path, [m.to_dict() for m in medias], mode="w")

        snapshots = []
        for media in medias:
            if self._should_snapshot(media, last_fetched.get(media.id), now):
                snap = {col: media.to_dict().get(col) for col in _SNAPSHOT_COLS}
                snapshots.append(snap)

        if snapshots:
            write(snap_path, snapshots, mode="a")

    def _write_stories(self, stories: list) -> None:
        path = os.path.join(self.data_dir, "stories.csv")
        if stories:
            write(path, [s.to_dict() for s in stories], mode="w")

    def _write_account(self, account) -> None:
        path = os.path.join(self.data_dir, "account_snapshots.csv")
        write(path, [account.to_dict()], mode="a")

    def _should_snapshot(self, media, last_fetched_str: str, now: datetime) -> bool:
        if last_fetched_str is None:
            return True
        try:
            last_fetched = datetime.fromisoformat(last_fetched_str)
            if last_fetched.tzinfo is None:
                last_fetched = last_fetched.replace(tzinfo=timezone.utc)
            post_ts = datetime.fromisoformat(media.timestamp)
            if post_ts.tzinfo is None:
                post_ts = post_ts.replace(tzinfo=timezone.utc)
        except ValueError:
            return True

        post_age = now - post_ts
        elapsed_since_last = now - last_fetched

        for max_age, interval in _PHASE_INTERVALS:
            if max_age is None or post_age <= max_age:
                return elapsed_since_last >= interval
        return False
