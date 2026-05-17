"""tests.test_instagram_controller"""
from unittest.mock import MagicMock, patch
from controllers.instagram_controller import InstagramController


class TestRun:
    def test_calls_service_run(self):
        mock_service = MagicMock()
        with patch("controllers.instagram_controller.InstagramService", return_value=mock_service):
            InstagramController().run()
        mock_service.run.assert_called_once()
