from goldshi.photo import pixels_to_ppm, ppm_to_pixels


def test_ppm_convert():
    image = b"P3\n3 2\n255\n255 0 0 0 255 0 0 0 255 255 255 0 255 255 255 0 0 0 "
    image2 = (
        b"P3\n3 2\n255\n132 122 9 0 23 0 254 0 250 32 192 57 203 162 222 109 71 22 "
    )

    assert pixels_to_ppm(ppm_to_pixels(image)) == image
    assert pixels_to_ppm(ppm_to_pixels(image2)) == image2
