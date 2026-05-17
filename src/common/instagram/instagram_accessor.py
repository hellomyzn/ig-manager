"""common.instagram.instagram_accessor"""
import requests as _requests
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from common.config import Config
from common.log import error, warn
from utils import Singleton

_ATTEMPTS = 3
_WAIT_SEC = 10
_TIMEOUT = 60


class InstagramAccessor(Singleton):
    """Instagram Graph API クライアント。"""

    _access_token: str = None
    _user_id: str = None
    _base_url: str = None

    def __init__(self):
        if self._access_token is not None:
            return
        config = Config().config["INSTAGRAM"]
        self._access_token = config["ACCESS_TOKEN"]
        self._user_id = config["USER_ID"]
        version = config["API_VERSION"]
        self._base_url = f"https://graph.facebook.com/{version}/"

    @property
    def user_id(self) -> str:
        return self._user_id

    def get(self, path: str, params: dict) -> dict:
        """Graph API に GET リクエストを送る。

        Args:
            path: エンドポイントパス（例: "me/media"）
            params: クエリパラメータ（access_token は自動付与）

        Returns:
            レスポンス JSON の dict
        """
        url = f"{self._base_url}{path}"
        all_params = {**params, "access_token": self._access_token}

        @retry(
            stop=stop_after_attempt(_ATTEMPTS),
            wait=wait_fixed(_WAIT_SEC),
            retry=retry_if_exception_type(_requests.ConnectionError),
            reraise=True,
        )
        def _call():
            resp = _requests.get(url, params=all_params, timeout=_TIMEOUT)
            if not resp.ok:
                error(
                    "Instagram API error {0} [{1}]: {2}",
                    resp.status_code, path, resp.text[:1000],
                )
                resp.raise_for_status()
            return resp.json()

        return _call()

    def parse_insights(self, response: dict) -> dict:
        """時系列 Insights レスポンスを {metric: value} の辞書に変換する。

        values リストの最新（末尾）の値を採用する。
        """
        result = {}
        for item in response.get("data", []):
            name = item.get("name")
            values = item.get("values", [])
            if name and values:
                result[name] = values[-1].get("value")
        return result

    def parse_total_value_insights(self, response: dict) -> dict:
        """metric_type=total_value のレスポンスを {metric: value} の辞書に変換する。

        total_value 形式: {"name": "profile_views", "total_value": {"value": 400}}
        """
        result = {}
        for item in response.get("data", []):
            name = item.get("name")
            total = item.get("total_value", {})
            if name and "value" in total:
                result[name] = total["value"]
        return result
