from goldshi.photo import (
    YCbCr_to_rgb,
    contrast,
    grayscale,
    pixels_to_ppm,
    ppm_to_pixels,
    rgb_to_YCbCr,
)


def main() -> None:
    with open("/home/saubuny/Pictures/ppm/goldshi.ppm", "rb") as f:
        image = f.read()

        try:
            output = ppm_to_pixels(image)
            output = rgb_to_YCbCr(output)
            output = contrast(output)
            output = YCbCr_to_rgb(output)
            output = pixels_to_ppm(output)
            with open("out", "wb") as out:
                out.write(output)
        except Exception as e:
            print(f"[Error] {e}")
