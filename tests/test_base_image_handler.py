"""Tests for BaseImageHandler.

Uses GIVEN/WHEN/THEN structure (Behaviour-Driven Development):
- GIVEN: the preconditions / setup state
- WHEN: the action under test is performed
- THEN: the expected outcome is asserted

This structure makes tests read like specifications, so anyone can
understand what the code is supposed to do without reading the implementation.
"""

from PIL import Image


class TestIsValidFileType:
    def test_accepts_jpg(self, base_handler):
        # GIVEN a filename with a .jpg extension
        # WHEN checking if it's a valid file type
        # THEN it should be accepted
        assert base_handler._is_valid_file_type("photo.jpg") is True

    def test_accepts_png(self, base_handler):
        assert base_handler._is_valid_file_type("photo.png") is True

    def test_accepts_jpeg(self, base_handler):
        assert base_handler._is_valid_file_type("photo.jpeg") is True

    def test_accepts_webp(self, base_handler):
        assert base_handler._is_valid_file_type("photo.webp") is True

    def test_rejects_unsupported_formats(self, base_handler):
        # GIVEN filenames with unsupported extensions
        # WHEN checking validity
        # THEN they should all be rejected
        assert base_handler._is_valid_file_type("photo.gif") is False
        assert base_handler._is_valid_file_type("photo.bmp") is False
        assert base_handler._is_valid_file_type("document.pdf") is False
        assert base_handler._is_valid_file_type("data.csv") is False

    def test_case_insensitive(self, base_handler):
        # GIVEN filenames with mixed-case extensions
        # WHEN checking validity
        # THEN case should not matter
        assert base_handler._is_valid_file_type("PHOTO.PNG") is True
        assert base_handler._is_valid_file_type("Photo.JpG") is True
        assert base_handler._is_valid_file_type("IMAGE.WEBP") is True

    def test_rejects_empty_string(self, base_handler):
        # GIVEN an empty filename
        # WHEN checking validity
        # THEN it should be rejected gracefully
        assert base_handler._is_valid_file_type("") is False

    def test_rejects_none(self, base_handler):
        # GIVEN a None value instead of a filename
        # WHEN checking validity
        # THEN it should be rejected without raising
        assert base_handler._is_valid_file_type(None) is False

    def test_rejects_no_extension(self, base_handler):
        # GIVEN a filename with no extension at all
        # WHEN checking validity
        # THEN it should be rejected
        assert base_handler._is_valid_file_type("filename") is False


class TestColourSub:
    def test_replaces_opaque_dark_pixels(self, base_handler):
        # GIVEN an image with one opaque dark pixel and one transparent pixel
        img = Image.new("RGBA", (2, 1), (0, 0, 0, 0))
        img.putdata([(50, 50, 50, 255), (50, 50, 50, 0)])
        red = (255, 0, 0, 255)

        # WHEN applying colour substitution
        result = base_handler._colour_sub(img, red)
        pixels = list(result.get_flattened_data())

        # THEN only the opaque dark pixel should be replaced
        assert pixels[0] == red
        assert pixels[1] == (50, 50, 50, 0)

    def test_skips_light_pixels(self, base_handler):
        # GIVEN an image with a light pixel (R >= 200)
        img = Image.new("RGBA", (1, 1), (220, 220, 220, 255))
        red = (255, 0, 0, 255)

        # WHEN applying colour substitution
        result = base_handler._colour_sub(img, red)
        pixels = list(result.get_flattened_data())

        # THEN light pixels should be left untouched (they're background/white areas)
        assert pixels[0] == (220, 220, 220, 255)

    def test_replaces_at_boundary(self, base_handler):
        # GIVEN a pixel with R=199 (just under the 200 threshold)
        img = Image.new("RGBA", (1, 1), (199, 100, 100, 255))
        blue = (0, 0, 255, 255)

        # WHEN applying colour substitution
        result = base_handler._colour_sub(img, blue)
        pixels = list(result.get_flattened_data())

        # THEN it should be replaced since 199 < 200
        assert pixels[0] == blue


class TestArchiveImage:
    def test_successful_archive(self, base_handler, monkeypatch):
        # GIVEN a file that can be moved
        calls = []
        monkeypatch.setattr("handling.base_image_handler.os.replace", lambda src, dst: calls.append((src, dst)))

        # WHEN archiving it
        base_handler._archive_image("test.png")

        # THEN it should be moved from img/ to img/zArchive/
        assert calls == [("img/test.png", "img/zArchive/test.png")]

    def test_os_error_is_logged(self, base_handler, monkeypatch):
        # GIVEN a file that can't be moved (e.g. locked by another process)
        monkeypatch.setattr(
            "handling.base_image_handler.os.replace", lambda s, d: (_ for _ in ()).throw(OSError("locked"))
        )
        logged = []
        monkeypatch.setattr(base_handler, "_append_ad_hoc_comment_to_log", lambda msg: logged.append(msg))

        # WHEN attempting to archive it
        base_handler._archive_image("test.png")

        # THEN the error should be logged instead of crashing
        assert len(logged) == 1
        assert "Unable to archive test.png" in logged[0]


class TestRenameFile:
    def test_successful_rename(self, base_handler, monkeypatch):
        # GIVEN a file that can be renamed
        monkeypatch.setattr("handling.base_image_handler.os.rename", lambda old, new: None)

        # WHEN renaming it
        # THEN it should return True to indicate success
        assert base_handler._rename_file("old.jpg", "new.png") is True

    def test_returns_false_when_target_exists(self, base_handler, monkeypatch):
        # GIVEN a target filename that already exists
        def raise_exists(old, new):
            raise FileExistsError

        monkeypatch.setattr("handling.base_image_handler.os.rename", raise_exists)
        monkeypatch.setattr(base_handler, "_append_ad_hoc_comment_to_log", lambda *a: None)

        # WHEN attempting to rename
        # THEN it should return False rather than crashing
        assert base_handler._rename_file("old.jpg", "existing.png") is False
