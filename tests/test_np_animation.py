"""Tests for np_animation module.

This module tests the color conversion functions and enumerators.
"""

import pytest
import sys
from unittest.mock import MagicMock
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock MicroPython modules that don't exist in regular Python
sys.modules["neopixel"] = MagicMock()
sys.modules["machine"] = MagicMock()
sys.modules["utime"] = MagicMock()

# Import directly from the module file
import np_animation as np_anim

to_grb = np_anim.to_grb
from_grb = np_anim.from_grb
hsl_to_rgb = np_anim.hsl_to_rgb
rgb_to_hsl = np_anim.rgb_to_hsl
rgb = np_anim.rgb
grb = np_anim.grb


class TestRGBGRBConversion:
    """Test RGB to GRB and GRB to RGB conversions."""

    def test_to_grb_basic(self):
        """Test converting RGB tuple to GRB bytes."""
        # Red
        assert to_grb((255, 0, 0)) == b"\x00\xff\x00"
        # Green
        assert to_grb((0, 255, 0)) == b"\xff\x00\x00"
        # Blue
        assert to_grb((0, 0, 255)) == b"\x00\x00\xff"
        # White
        assert to_grb((255, 255, 255)) == b"\xff\xff\xff"
        # Black
        assert to_grb((0, 0, 0)) == b"\x00\x00\x00"

    def test_to_grb_mixed_colors(self):
        """Test converting mixed RGB colors to GRB bytes."""
        # Yellow (R+G)
        assert to_grb((255, 255, 0)) == b"\xff\xff\x00"
        # Cyan (G+B)
        assert to_grb((0, 255, 255)) == b"\xff\x00\xff"
        # Magenta (R+B)
        assert to_grb((255, 0, 255)) == b"\x00\xff\xff"
        # Orange
        assert to_grb((252, 102, 3)) == b"\x66\xfc\x03"

    def test_from_grb_basic(self):
        """Test converting GRB bytes to RGB tuple."""
        # Red
        assert from_grb(b"\x00\xff\x00") == (255, 0, 0)
        # Green
        assert from_grb(b"\xff\x00\x00") == (0, 255, 0)
        # Blue
        assert from_grb(b"\x00\x00\xff") == (0, 0, 255)
        # White
        assert from_grb(b"\xff\xff\xff") == (255, 255, 255)
        # Black
        assert from_grb(b"\x00\x00\x00") == (0, 0, 0)

    def test_from_grb_mixed_colors(self):
        """Test converting mixed GRB colors to RGB tuple."""
        # Orange
        assert from_grb(b"\x66\xfc\x03") == (252, 102, 3)
        # Gray
        assert from_grb(b"\x7f\x7f\x7f") == (127, 127, 127)
        # Dark red
        assert from_grb(b"\x00\x44\x00") == (68, 0, 0)

    def test_rgb_grb_round_trip(self):
        """Test that RGB -> GRB -> RGB conversions are lossless."""
        test_colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 255),
            (0, 0, 0),
            (127, 127, 127),
            (252, 102, 3),
            (100, 150, 200),
        ]
        for color in test_colors:
            grb_bytes = to_grb(color)
            rgb_tuple = from_grb(grb_bytes)
            assert rgb_tuple == color, f"Round trip failed for {color}"


class TestRGBHSLConversion:
    """Test RGB to HSL and HSL to RGB conversions."""

    def test_hsl_to_rgb_primary_colors(self):
        """Test converting HSL to RGB for primary colors."""
        # Red (H=0, S=100, L=50)
        r, g, b = hsl_to_rgb(0, 100, 50)
        assert (
            r == 255 and abs(g) <= 3 and abs(b) <= 3
        ), f"Expected (255, 0, 0), got ({r}, {g}, {b})"

        # Green (H=120, S=100, L=50)
        r, g, b = hsl_to_rgb(120, 100, 50)
        assert (
            abs(r) <= 3 and g == 255 and abs(b) <= 3
        ), f"Expected (0, 255, 0), got ({r}, {g}, {b})"

        # Blue (H=240, S=100, L=50)
        r, g, b = hsl_to_rgb(240, 100, 50)
        assert (
            abs(r) <= 3 and abs(g) <= 3 and b == 255
        ), f"Expected (0, 0, 255), got ({r}, {g}, {b})"

    def test_hsl_to_rgb_achromatic(self):
        """Test converting HSL to RGB for colors without saturation."""
        # White (any H, S=0, L=100)
        result = hsl_to_rgb(0, 0, 100)
        assert result == (255, 255, 255), f"Expected (255, 255, 255), got {result}"

        # Black (any H, S=0, L=0)
        result = hsl_to_rgb(0, 0, 0)
        assert result == (0, 0, 0), f"Expected (0, 0, 0), got {result}"

        # Gray (any H, S=0, L=50)
        result = hsl_to_rgb(0, 0, 50)
        # Should be approximately (127, 127, 127)
        assert all(
            c in range(127, 129) for c in result
        ), f"Expected ~(127, 127, 127), got {result}"

    def test_rgb_to_hsl_primary_colors(self):
        """Test converting RGB to HSL for primary colors."""
        # Red
        h, s, l = rgb_to_hsl(255, 0, 0)
        assert (
            h == 0 and s == 100 and l == 50
        ), f"Expected (0, 100, 50), got ({h}, {s}, {l})"

        # Green
        h, s, l = rgb_to_hsl(0, 255, 0)
        assert (
            h == 120 and s == 100 and l == 50
        ), f"Expected (120, 100, 50), got ({h}, {s}, {l})"

        # Blue
        h, s, l = rgb_to_hsl(0, 0, 255)
        assert (
            h == 240 and s == 100 and l == 50
        ), f"Expected (240, 100, 50), got ({h}, {s}, {l})"

    def test_rgb_to_hsl_achromatic(self):
        """Test converting RGB to HSL for grayscale colors."""
        # White
        h, s, l = rgb_to_hsl(255, 255, 255)
        assert s == 0 and l == 100, f"Expected (*, 0, 100), got ({h}, {s}, {l})"

        # Black
        h, s, l = rgb_to_hsl(0, 0, 0)
        assert s == 0 and l == 0, f"Expected (*, 0, 0), got ({h}, {s}, {l})"

        # Gray
        h, s, l = rgb_to_hsl(127, 127, 127)
        assert s == 0, f"Expected saturation 0, got {s}"
        # Lightness should be around 50
        assert 49 <= l <= 51, f"Expected lightness ~50, got {l}"

    def test_hsl_rgb_round_trip(self):
        """Test that HSL -> RGB -> HSL conversions preserve values (approximately)."""
        test_colors_hsl = [
            (0, 100, 50),  # Red
            (120, 100, 50),  # Green
            (240, 100, 50),  # Blue
            (60, 100, 50),  # Yellow
            (180, 100, 50),  # Cyan
            (300, 100, 50),  # Magenta
        ]

        for h, s, l in test_colors_hsl:
            rgb_val = hsl_to_rgb(h, s, l)
            h2, s2, l2 = rgb_to_hsl(*rgb_val)
            # Allow small tolerance due to rounding
            assert abs(h - h2) <= 1, f"Hue mismatch: {h} -> {h2}"
            assert abs(s - s2) <= 2, f"Saturation mismatch: {s} -> {s2}"
            assert abs(l - l2) <= 2, f"Lightness mismatch: {l} -> {l2}"

    def test_rgb_hsl_round_trip(self):
        """Test that RGB -> HSL -> RGB conversions preserve values (approximately)."""
        test_colors_rgb = [
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (0, 255, 255),  # Cyan
            (255, 0, 255),  # Magenta
            (128, 128, 128),  # Gray
        ]

        for r, g, b in test_colors_rgb:
            hsl_val = rgb_to_hsl(r, g, b)
            r2, g2, b2 = hsl_to_rgb(*hsl_val)
            # Allow small tolerance due to rounding
            assert abs(r - r2) <= 4, f"Red mismatch: {r} -> {r2}"
            assert abs(g - g2) <= 4, f"Green mismatch: {g} -> {g2}"
            assert abs(b - b2) <= 4, f"Blue mismatch: {b} -> {b2}"


class TestGRBEnum:
    """Test the grb color enumerator."""

    def test_grb_black_variants(self):
        """Test that BLACK, NONE, and OFF are the same."""
        assert grb.BLACK == grb.NONE == grb.OFF
        assert grb.BLACK == b"\x00\x00\x00"

    def test_grb_primary_colors(self):
        """Test primary color values in GRB format."""
        # Red should be (g=0, r=255, b=0)
        assert grb.RED == b"\x00\xff\x00"
        # Green should be (g=255, r=0, b=0)
        assert grb.GREEN == b"\xff\x00\x00"
        # Blue should be (g=0, r=0, b=255)
        assert grb.BLUE == b"\x00\x00\xff"

    def test_grb_mixed_colors(self):
        """Test mixed color values in GRB format."""
        assert grb.WHITE == b"\xff\xff\xff"
        assert grb.YELLOW == b"\xff\xff\x00"  # (g=255, r=255, b=0)
        assert grb.CYAN == b"\xff\x00\xff"  # (g=255, r=0, b=255)
        assert grb.MAGENTA == b"\x00\xff\xff"  # (g=0, r=255, b=255)

    def test_grb_special_colors(self):
        """Test special color values in GRB format."""
        assert grb.ORANGE == b"\x66\xfc\x03"
        assert grb.DARK_RED == b"\x00\x44\x00"
        assert grb.VIOLET == b"\x7f\x7f\xff"
        assert grb.GRAY == b"\x7f\x7f\x7f"

    def test_grb_all_are_bytes(self):
        """Test that all grb enum values are bytes type."""
        attrs = [attr for attr in dir(grb) if not attr.startswith("_")]
        for attr in attrs:
            value = getattr(grb, attr)
            assert isinstance(
                value, bytes
            ), f"{attr} should be bytes, got {type(value)}"
            assert len(value) == 3, f"{attr} should have 3 bytes, got {len(value)}"


class TestRGBEnum:
    """Test the rgb color enumerator."""

    def test_rgb_black_variants(self):
        """Test that BLACK, NONE, and OFF are the same."""
        assert rgb.BLACK == rgb.NONE == rgb.OFF
        assert rgb.BLACK == (0, 0, 0)

    def test_rgb_primary_colors(self):
        """Test primary color values in RGB format."""
        assert rgb.RED == (255, 0, 0)
        assert rgb.GREEN == (0, 255, 0)
        assert rgb.BLUE == (0, 0, 255)

    def test_rgb_mixed_colors(self):
        """Test mixed color values in RGB format."""
        assert rgb.WHITE == (255, 255, 255)
        assert rgb.YELLOW == (255, 255, 0)
        assert rgb.CYAN == (0, 255, 255)
        assert rgb.MAGENTA == (255, 0, 255)

    def test_rgb_special_colors(self):
        """Test special color values in RGB format."""
        assert rgb.ORANGE == (252, 102, 3)
        assert rgb.DARK_RED == (68, 0, 0)
        assert rgb.VIOLET == (127, 127, 255)
        assert rgb.GRAY == (127, 127, 127)

    def test_rgb_all_are_tuples(self):
        """Test that all rgb enum values are tuple type."""
        attrs = [attr for attr in dir(rgb) if not attr.startswith("_")]
        for attr in attrs:
            value = getattr(rgb, attr)
            assert isinstance(
                value, tuple
            ), f"{attr} should be tuple, got {type(value)}"
            assert len(value) == 3, f"{attr} should have 3 elements, got {len(value)}"
            # All values should be integers between 0-255
            for component in value:
                assert isinstance(component, int), f"RGB component should be int"
                assert (
                    0 <= component <= 255
                ), f"RGB component should be 0-255, got {component}"

    def test_rgb_grb_correspondence(self):
        """Test that rgb enum values correspond correctly to grb enum values."""
        # Test that converting grb enum to rgb gives the rgb enum
        assert from_grb(grb.RED) == rgb.RED
        assert from_grb(grb.GREEN) == rgb.GREEN
        assert from_grb(grb.BLUE) == rgb.BLUE
        assert from_grb(grb.WHITE) == rgb.WHITE
        assert from_grb(grb.BLACK) == rgb.BLACK
        assert from_grb(grb.YELLOW) == rgb.YELLOW
        assert from_grb(grb.CYAN) == rgb.CYAN
        assert from_grb(grb.MAGENTA) == rgb.MAGENTA
        assert from_grb(grb.ORANGE) == rgb.ORANGE
        assert from_grb(grb.DARK_RED) == rgb.DARK_RED
        assert from_grb(grb.VIOLET) == rgb.VIOLET
        assert from_grb(grb.GRAY) == rgb.GRAY

        # Test that converting rgb enum to grb gives the grb enum
        assert to_grb(rgb.RED) == grb.RED
        assert to_grb(rgb.GREEN) == grb.GREEN
        assert to_grb(rgb.BLUE) == grb.BLUE
        assert to_grb(rgb.WHITE) == grb.WHITE
        assert to_grb(rgb.BLACK) == grb.BLACK


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
