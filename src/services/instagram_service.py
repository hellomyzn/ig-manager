"""services.instagram_service"""
import os
from dataclasses import dataclass

from common.csv import write
from common.log import info
from repositories.instagram_repository import InstagramRepository

_DEFAULT_DATA_DIR = os.environ.get("DATA_DIR", "data")

_SNAPSHOT_COLS = [
    "id", "fetched_at", "like_count", "comments_count",
    "reach", "saved", "shares",
    "profile_visits", "follows", "total_interactions",
]


@dataclass
class InstagramService:
    data_dir: str = _DEFAULT_DATA_DIR

    def __post_init__(self):
        os.makedirs(self.data_dir, exist_ok=True)
        self._repo = InstagramRepository()

    def run(self) -> None:
        info("Instagram data fetch started")

        medias = self._repo.fetch_medias()
        account = self._repo.fetch_account()

        self._write_medias(medias)
        self._write_account(account)

        info("Instagram data fetch completed")

    def _write_medias(self, medias: list) -> None:
        media_path = os.path.join(self.data_dir, "media.csv")
        snap_path = os.path.join(self.data_dir, "media_snapshots.csv")

        write(media_path, [m.to_dict() for m in medias], mode="w")

        snapshots = [{col: m.to_dict().get(col) for col in _SNAPSHOT_COLS} for m in medias]
        write(snap_path, snapshots, mode="a")

    def _write_account(self, account) -> None:
        path = os.path.join(self.data_dir, "account_snapshots.csv")
        write(path, [account.to_dict()], mode="a")
