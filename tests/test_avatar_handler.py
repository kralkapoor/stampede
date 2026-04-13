"""Tests for AvatarHandler.

Uses GIVEN/WHEN/THEN structure (Behaviour-Driven Development):
- GIVEN: the preconditions / setup state
- WHEN: the action under test is performed
- THEN: the expected outcome is asserted
"""

import logging
from unittest.mock import MagicMock

from handling.avatar_base_handler import AvatarBaseHandler


class TestExecuteModelRequest:
    def _make_mock_image(self, name):
        """Helper to create a mock file object with a .name attribute."""
        img = MagicMock()
        img.name = name
        return img

    def test_successful_results_collected(self, avatar_handler, mock_openai_response, monkeypatch):
        # GIVEN one input image and a successful API response
        mock_image = self._make_mock_image("img/test.png")
        monkeypatch.setattr(AvatarBaseHandler, "_execute_edit_request", lambda self, p, i: mock_openai_response)
        monkeypatch.setattr(avatar_handler, "_save_avatars", lambda x: None)

        # WHEN executing the model request
        result = avatar_handler._execute_model_requests("prompt", [mock_image])

        # THEN the result should contain the filename paired with the response
        assert len(result) == 1
        assert result[0] == ("test.png", mock_openai_response)

    def test_none_results_skipped(self, avatar_handler, monkeypatch):
        # GIVEN one input image and an API that returns None (failure)
        mock_image = self._make_mock_image("img/failed.png")
        monkeypatch.setattr(AvatarBaseHandler, "_execute_edit_request", lambda self, p, i: None)
        monkeypatch.setattr(avatar_handler, "_save_avatars", lambda x: None)

        # WHEN executing the model request
        result = avatar_handler._execute_model_requests("prompt", [mock_image])

        # THEN no results should be collected
        assert len(result) == 0

    def test_mixed_success_and_failure(self, avatar_handler, mock_openai_response, monkeypatch):
        # GIVEN two images where the first succeeds and the second fails
        img_ok = self._make_mock_image("img/good.png")
        img_fail = self._make_mock_image("img/bad.png")
        responses = {"img/good.png": mock_openai_response, "img/bad.png": None}
        monkeypatch.setattr(AvatarBaseHandler, "_execute_edit_request", lambda self, p, i: responses[i.name])
        monkeypatch.setattr(avatar_handler, "_save_avatars", lambda x: None)

        # WHEN executing the model request
        result = avatar_handler._execute_model_requests("prompt", [img_ok, img_fail])

        # THEN only the successful result should be collected
        assert len(result) == 1
        assert result[0][0] == "good.png"

    def test_failure_is_logged(self, avatar_handler, monkeypatch, caplog):
        # GIVEN an input image and an API that returns None
        mock_image = self._make_mock_image("img/broken.png")
        monkeypatch.setattr(AvatarBaseHandler, "_execute_edit_request", lambda self, p, i: None)
        monkeypatch.setattr(avatar_handler, "_save_avatars", lambda x: None)

        # WHEN executing the model request
        with caplog.at_level(logging.ERROR):
            avatar_handler._execute_model_requests("prompt", [mock_image])

        # THEN the failure should be logged with the filename
        assert "broken.png" in caplog.text
