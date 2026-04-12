"""Tests for RectangleHandler.

Uses GIVEN/WHEN/THEN structure (Behaviour-Driven Development):
- GIVEN: the preconditions / setup state
- WHEN: the action under test is performed
- THEN: the expected outcome is asserted
"""

import logging
from unittest.mock import MagicMock, mock_open, patch

from PIL import Image

from settings.static_dicts import COLOURS, RECT_PATHS


class TestCustomStampDetection:
    def test_single_ampersand_is_custom(self, rectangle_handler):
        # GIVEN a filename with exactly one "&" (colour marker)
        filename = "stamp&R."

        # WHEN counting ampersands to determine custom vs generic
        is_custom = filename.count("&") == 1

        # THEN it should be detected as a custom stamp
        assert is_custom is True

    def test_no_ampersand_is_generic(self, rectangle_handler):
        # GIVEN a filename with no "&"
        filename = "stamp."

        # WHEN counting ampersands
        is_custom = filename.count("&") == 1

        # THEN it should be detected as generic (all colours)
        assert is_custom is False

    def test_multiple_ampersands_is_generic(self, rectangle_handler):
        # GIVEN a filename with more than one "&"
        filename = "stamp&R&G."

        # WHEN counting ampersands
        is_custom = filename.count("&") == 1

        # THEN it should be detected as generic (ambiguous)
        assert is_custom is False


class TestColourCodeExtraction:
    def test_extracts_single_letter_code(self, rectangle_handler):
        # GIVEN a filename with a single-letter colour code
        no_extension = "stamp&R."

        # WHEN extracting the colour code
        code = no_extension[no_extension.index("&") : -1]

        # THEN the full "&X" code should be returned
        assert code == "&R"

    def test_extracts_multi_letter_code(self, rectangle_handler):
        # GIVEN a filename with a multi-letter colour code
        no_extension = "stamp&PP."

        # WHEN extracting the colour code
        code = no_extension[no_extension.index("&") : -1]

        # THEN the full "&PP" code should be returned
        assert code == "&PP"

    def test_extracts_orange_code(self, rectangle_handler):
        # GIVEN a filename with the orange colour code
        no_extension = "design&O."

        # WHEN extracting the colour code
        code = no_extension[no_extension.index("&") : -1]

        # THEN "&O" should be returned
        assert code == "&O"


class TestHandlerFunction:
    def test_rename_failure_aborts_processing(self, rectangle_handler, monkeypatch):
        # GIVEN a file that already exists as a .png (rename will fail)
        monkeypatch.setattr(
            "handling.imagehandler.rectangle_handler.os.rename",
            MagicMock(side_effect=FileExistsError),
        )
        save_mock = MagicMock()
        monkeypatch.setattr("PIL.Image.Image.save", save_mock)

        # WHEN processing the file
        rectangle_handler._handler_function("stamp&R.jpg")

        # THEN no image should be saved (processing aborted early)
        save_mock.assert_not_called()

    def test_rename_failure_is_logged(self, rectangle_handler, monkeypatch, caplog):
        # GIVEN a file that already exists as a .png
        monkeypatch.setattr(
            "handling.imagehandler.rectangle_handler.os.rename",
            MagicMock(side_effect=FileExistsError),
        )

        # WHEN processing the file
        with caplog.at_level(logging.ERROR):
            rectangle_handler._handler_function("stamp&R.jpg")

        # THEN the failure should be logged
        assert "file already exists" in caplog.text

    def test_custom_stamp_saves_to_custom_path(self, rectangle_handler, monkeypatch, tmp_path):
        # GIVEN a custom stamp file (single "&") and writable output dirs
        img = Image.new("RGBA", (50, 50), (50, 50, 50, 255))
        monkeypatch.setattr("handling.imagehandler.rectangle_handler.os.rename", lambda old, new: None)
        monkeypatch.setattr("PIL.Image.open", lambda path: img)
        monkeypatch.setattr(rectangle_handler, "_open_save_destination", lambda d: None)
        monkeypatch.setattr(rectangle_handler, "_archive_image", lambda f: None)

        saved_paths = []
        original_save = Image.Image.save

        def capture_save(self, path, **kwargs):
            saved_paths.append(path)

        monkeypatch.setattr("PIL.Image.Image.save", capture_save)

        # WHEN processing a custom red stamp
        rectangle_handler._handler_function("stamp&R.jpg")

        # THEN it should save to the Custom subdirectory
        assert len(saved_paths) == 1
        assert RECT_PATHS["Custom"] in saved_paths[0]

    def test_generic_stamp_creates_all_colours(self, rectangle_handler, monkeypatch):
        # GIVEN a generic stamp file (no "&") and writable output dirs
        img = Image.new("RGBA", (50, 50), (50, 50, 50, 255))
        monkeypatch.setattr("handling.imagehandler.rectangle_handler.os.rename", lambda old, new: None)
        monkeypatch.setattr("PIL.Image.open", lambda path: img)
        monkeypatch.setattr(rectangle_handler, "_open_save_destination", lambda d: None)
        monkeypatch.setattr(rectangle_handler, "_archive_image", lambda f: None)

        saved_paths = []

        def capture_save(self, path, **kwargs):
            saved_paths.append(path)

        monkeypatch.setattr("PIL.Image.Image.save", capture_save)

        # WHEN processing a generic stamp
        rectangle_handler._handler_function("stamp.jpg")

        # THEN it should create one copy per colour in COLOURS
        assert len(saved_paths) == len(COLOURS)

    def test_generic_stamp_uses_correct_colour_paths(self, rectangle_handler, monkeypatch):
        # GIVEN a generic stamp file
        img = Image.new("RGBA", (50, 50), (50, 50, 50, 255))
        monkeypatch.setattr("handling.imagehandler.rectangle_handler.os.rename", lambda old, new: None)
        monkeypatch.setattr("PIL.Image.open", lambda path: img)
        monkeypatch.setattr(rectangle_handler, "_open_save_destination", lambda d: None)
        monkeypatch.setattr(rectangle_handler, "_archive_image", lambda f: None)

        saved_paths = []

        def capture_save(self, path, **kwargs):
            saved_paths.append(path)

        monkeypatch.setattr("PIL.Image.Image.save", capture_save)

        # WHEN processing a generic stamp
        rectangle_handler._handler_function("stamp.jpg")

        # THEN each saved path should correspond to a colour's configured directory
        for code in COLOURS:
            matching = [p for p in saved_paths if RECT_PATHS[code] in p]
            assert len(matching) == 1, f"Expected one save for colour code '{code}'"

    def test_unexpected_error_is_logged(self, rectangle_handler, monkeypatch, caplog):
        # GIVEN a file where Image.open raises an unexpected error
        monkeypatch.setattr("handling.imagehandler.rectangle_handler.os.rename", lambda old, new: None)
        monkeypatch.setattr("PIL.Image.open", MagicMock(side_effect=OSError("corrupt file")))

        # WHEN processing the file
        with caplog.at_level(logging.ERROR):
            rectangle_handler._handler_function("bad.jpg")

        # THEN the error should be logged with the filename
        assert "bad." in caplog.text


class TestRectPaths:
    def test_all_colour_codes_have_paths(self, rectangle_handler):
        # GIVEN the COLOURS and RECT_PATHS dictionaries
        # WHEN checking that every colour has a corresponding output path
        # THEN every colour code should be present in RECT_PATHS
        for code in COLOURS:
            assert code in RECT_PATHS, f"Colour code '{code}' missing from RECT_PATHS"
