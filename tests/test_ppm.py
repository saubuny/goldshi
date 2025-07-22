import re
from goldshi.photo import ppm_to_pixels
import pytest


def test_ppm_to_pixels_incorrect_format():
    should_fail = "P1 2 2 255 125 0 143 133 3 100 32 44 55 98 208 179".encode("utf-8")

    with pytest.raises(Exception, match=re.escape("Only the P3 format is supported")):
        ppm_to_pixels(should_fail)


def test_ppm_to_pixels_rgb_value_overflow():
    should_fail = "P3 2 2 255 125 0 143 133 3 355 32 44 55 98 208 179".encode("utf-8")
    with pytest.raises(Exception, match=re.escape("Invalid PPM file given")):
        ppm_to_pixels(should_fail)
