from goldshi.photo import ppm_to_pixels


def main() -> None:
    with open("/home/saubuny/Pictures/goldshi.ppm", "rb") as f:
        image = f.read()

        try:
            ppm_to_pixels(image)
        except Exception as e:
            print(f"[Error] {e}")
