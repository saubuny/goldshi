from goldshi.cli import cli


def main() -> None:
    # with open("/home/saubuny/Pictures/ppm/teto.ppm", "rb") as f:
    #     image = f.read()
    #
    #     try:
    #         output = ppm_to_pixels(image)
    #         # output = rgb_to_YCbCr(output)
    #         # output = resize(output, 1920, 1080)
    #         output = mirror_vertical(output)
    #         output = mirror_horizontal(output)
    #         # output = YCbCr_to_rgb(output)
    #         output = pixels_to_ppm(output)
    #         with open("out", "wb") as out:
    #             out.write(output)
    #     except Exception:
    #         print(traceback.format_exc())
    cli()
