from goldshi.photo import Pixels, newPixels, rgb_to_YCbCr, YCbCr_to_rgb


def test_rgb_YCbCr_convert():
    rgb_pixels: Pixels = [
        [[0.5, 0.4, 1.0], [0.2, 0.12, 0.293423]],
        [[0.3, 0.324, 0.012], [0.0012, 0.91232, 0.0]],
    ]
    assert rgb_pixels == YCbCr_to_rgb(rgb_to_YCbCr(rgb_pixels))
