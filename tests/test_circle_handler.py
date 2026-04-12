"""Tests for CircleHandler.

Uses GIVEN/WHEN/THEN structure (Behaviour-Driven Development):
- GIVEN: the preconditions / setup state
- WHEN: the action under test is performed
- THEN: the expected outcome is asserted
"""

from PIL import Image


class TestCheckIsColoured:
    def test_single_ampersand_means_coloured(self, circle_handler):
        # GIVEN a filename containing exactly one "&" (colour marker)
        # WHEN checking if it's coloured
        # THEN it should return True
        assert circle_handler.check_is_coloured("stamp&R.") is True
        assert circle_handler.check_is_coloured("design&B.") is True

    def test_no_ampersand_means_not_coloured(self, circle_handler):
        # GIVEN a filename with no "&"
        # WHEN checking if it's coloured
        # THEN it should return False (will be processed as black/white)
        assert circle_handler.check_is_coloured("stamp.") is False

    def test_multiple_ampersands_means_not_coloured(self, circle_handler):
        # GIVEN a filename with more than one "&"
        # WHEN checking if it's coloured
        # THEN it should return False (ambiguous, treat as uncoloured)
        assert circle_handler.check_is_coloured("stamp&R&G.") is False


class TestDetermineColourExtension:
    def test_extracts_single_letter_codes(self, circle_handler):
        # GIVEN filenames with single-letter colour codes after "&"
        # WHEN extracting the colour extension
        # THEN the "&" prefix and code should be returned
        assert circle_handler.determine_colour_extension("stamp&R.") == "&R"
        assert circle_handler.determine_colour_extension("file&B.") == "&B"

    def test_extracts_multi_letter_codes(self, circle_handler):
        # GIVEN filenames with multi-letter colour codes (e.g. PP, E)
        # WHEN extracting the colour extension
        # THEN the full code should be returned
        assert circle_handler.determine_colour_extension("design&PP.") == "&PP"
        assert circle_handler.determine_colour_extension("x&E.") == "&E"


class TestResize:
    def test_output_is_rgba(self, circle_handler):
        # GIVEN a standard RGBA input image
        img = Image.new("RGBA", (100, 100), (0, 0, 0, 255))

        # WHEN resizing with circular mask
        result = circle_handler.resize(img)

        # THEN the output should still be RGBA (needed for transparency)
        assert result.mode == "RGBA"

    def test_corners_are_transparent(self, circle_handler):
        # GIVEN a solid opaque input image
        img = Image.new("RGBA", (100, 100), (0, 0, 0, 255))

        # WHEN applying the circular mask
        result = circle_handler.resize(img)

        # THEN corners should be transparent (outside the circle)
        corner_pixel = result.getpixel((0, 0))
        assert corner_pixel[3] == 0

    def test_centre_is_opaque(self, circle_handler):
        # GIVEN a solid opaque input image
        img = Image.new("RGBA", (100, 100), (50, 50, 50, 255))

        # WHEN applying the circular mask
        result = circle_handler.resize(img)

        # THEN the centre should remain opaque (inside the circle)
        cx, cy = result.size[0] // 2, result.size[1] // 2
        centre_pixel = result.getpixel((cx, cy))
        assert centre_pixel[3] == 255


class TestStandardiseSize:
    def test_auto_detects_from_smallest_dimension(self, circle_handler):
        # GIVEN standard_size is not configured (None)
        circle_handler.standard_size = None
        img = Image.new("RGBA", (200, 150), (0, 0, 0, 255))

        # WHEN standardising size
        result = circle_handler._standardise_size(img)

        # THEN it should use the smallest dimension as a square
        assert result.size == (150, 150)

    def test_uses_explicit_configured_size(self, circle_handler):
        # GIVEN a specific standard_size is configured
        circle_handler.standard_size = (80, 80)
        img = Image.new("RGBA", (200, 200), (0, 0, 0, 255))

        # WHEN standardising size
        result = circle_handler._standardise_size(img)

        # THEN it should resize to exactly that size
        assert result.size == (80, 80)
