"""tests.test_instagram_accessor"""
from unittest.mock import patch, MagicMock
import pytest
from common.instagram.instagram_accessor import InstagramAccessor


@pytest.fixture
def accessor(reset_singletons):
    with patch("common.instagram.instagram_accessor.Config") as MockConfig:
        cfg = MagicMock()
        cfg.__getitem__.side_effect = lambda s: {
            "INSTAGRAM": {"ACCESS_TOKEN": "tok", "USER_ID": "uid", "API_VERSION": "v21.0"}
        }[s]
        MockConfig.return_value.config = cfg
        acc = InstagramAccessor()
    return acc


class TestGet:
    def test_calls_request_get_with_correct_url(self, accessor):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {"data": []}
        with patch("common.instagram.instagram_accessor._requests.get", return_value=mock_resp) as mock_get:
            accessor.get("me/media", {"fields": "id"})
        mock_get.assert_called_once()
        url = mock_get.call_args[0][0]
        assert "graph.facebook.com" in url
        assert "me/media" in url

    def test_access_token_appended_to_params(self, accessor):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {}
        with patch("common.instagram.instagram_accessor._requests.get", return_value=mock_resp) as mock_get:
            accessor.get("me", {})
        params = mock_get.call_args[1]["params"]
        assert params["access_token"] == "tok"


class TestParseInsights:
    def test_converts_response_to_flat_dict(self, accessor):
        response = {
            "data": [
                {"name": "reach", "values": [{"value": 100}]},
                {"name": "impressions", "values": [{"value": 200}]},
            ]
        }
        result = accessor.parse_insights(response)
        assert result == {"reach": 100, "impressions": 200}

    def test_uses_last_value_for_timeseries(self, accessor):
        response = {
            "data": [
                {"name": "reach", "values": [{"value": 100}, {"value": 200}]},
            ]
        }
        assert accessor.parse_insights(response)["reach"] == 200

    def test_returns_empty_dict_for_empty_data(self, accessor):
        assert accessor.parse_insights({"data": []}) == {}

    def test_returns_empty_dict_for_missing_data_key(self, accessor):
        assert accessor.parse_insights({}) == {}


class TestParseTotalValueInsights:
    def test_converts_total_value_response(self, accessor):
        response = {
            "data": [
                {"name": "profile_views", "total_value": {"value": 400}},
                {"name": "website_clicks", "total_value": {"value": 30}},
            ]
        }
        result = accessor.parse_total_value_insights(response)
        assert result == {"profile_views": 400, "website_clicks": 30}

    def test_returns_empty_dict_for_empty_data(self, accessor):
        assert accessor.parse_total_value_insights({"data": []}) == {}

    def test_ignores_items_without_value(self, accessor):
        response = {"data": [{"name": "x", "total_value": {}}]}
        assert accessor.parse_total_value_insights(response) == {}
