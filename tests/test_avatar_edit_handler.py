"""Tests for AvatarEditHandler.

Uses GIVEN/WHEN/THEN structure (Behaviour-Driven Development):
- GIVEN: the preconditions / setup state
- WHEN: the action under test is performed
- THEN: the expected outcome is asserted
"""

import pytest


class TestValidateSingleImage:
    def test_one_image_returns_filename(self, avatar_edit_handler, monkeypatch):
        # GIVEN exactly one valid image file in the img directory
        monkeypatch.setattr("handling.avatar_edit_handler.os.listdir", lambda _: ["avatar.png"])

        # WHEN validating
        result = avatar_edit_handler.validate_single_image()

        # THEN the filename should be returned
        assert result == "avatar.png"

    def test_no_images_raises(self, avatar_edit_handler, monkeypatch):
        # GIVEN an empty img directory
        monkeypatch.setattr("handling.avatar_edit_handler.os.listdir", lambda _: [])

        # WHEN validating
        # THEN a ValueError should be raised with a helpful message
        with pytest.raises(ValueError, match="No image found"):
            avatar_edit_handler.validate_single_image()

    def test_multiple_images_raises_with_count(self, avatar_edit_handler, monkeypatch):
        # GIVEN three image files in the img directory
        monkeypatch.setattr("handling.avatar_edit_handler.os.listdir", lambda _: ["a.png", "b.jpg", "c.webp"])

        # WHEN validating
        # THEN a ValueError should include the count so the user knows how many to remove
        with pytest.raises(ValueError, match="3 images"):
            avatar_edit_handler.validate_single_image()

    def test_filters_non_image_files(self, avatar_edit_handler, monkeypatch):
        # GIVEN a mix of image and non-image files
        monkeypatch.setattr(
            "handling.avatar_edit_handler.os.listdir", lambda _: ["readme.txt", "avatar.png", ".gitkeep"]
        )

        # WHEN validating
        # THEN only the image file should be considered
        result = avatar_edit_handler.validate_single_image()
        assert result == "avatar.png"

    def test_only_non_image_files_raises(self, avatar_edit_handler, monkeypatch):
        # GIVEN only non-image files in the directory
        monkeypatch.setattr("handling.avatar_edit_handler.os.listdir", lambda _: ["readme.txt", ".gitkeep"])

        # WHEN validating
        # THEN it should raise as if the directory were empty
        with pytest.raises(ValueError, match="No image found"):
            avatar_edit_handler.validate_single_image()
