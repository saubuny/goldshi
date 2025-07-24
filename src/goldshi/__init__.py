from goldshi.photo import box_blur, pixels_to_ppm, ppm_to_pixels


def main() -> None:
    with open("/home/saubuny/Pictures/goldshi.ppm", "rb") as f:
        image = f.read()

        try:
            output = pixels_to_ppm(box_blur(ppm_to_pixels(image)))
            with open("out", "wb") as out:
                out.write(output)
        except Exception as e:
            print(f"[Error] {e}")
