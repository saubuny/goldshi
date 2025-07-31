from goldshi.photo import (
    YCbCr_to_rgb,
    brightness,
    contrast,
    grayscale,
    pixels_to_ppm,
    ppm_to_pixels,
    resize_x,
    resize_y,
    rgb_to_YCbCr,
)
import traceback


def main() -> None:
    with open("/home/saubuny/Pictures/ppm/goldshi.ppm", "rb") as f:
        image = f.read()

        try:
            output = ppm_to_pixels(image)
            # output = rgb_to_YCbCr(output)
            output = resize_y(output, 20)
            # output = YCbCr_to_rgb(output)
            output = pixels_to_ppm(output)
            with open("out", "wb") as out:
                out.write(output)
        except Exception:
            print(traceback.format_exc())
