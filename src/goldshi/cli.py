import argparse

from goldshi.photo import (
    YCbCr_to_rgb,
    box_blur,
    brightness,
    contrast,
    grayscale,
    mirror_horizontal,
    mirror_vertical,
    pixels_to_ppm,
    ppm_to_pixels,
    rgb_to_YCbCr,
)


def cli():
    parser = argparse.ArgumentParser()

    parser.add_argument("image_path", help="path to image")
    parser.add_argument(
        "-v", "--verbose", help="include a progress bar", action="store_true"
    )
    parser.add_argument(
        "-b",
        "--brightness",
        type=float,
        help="change in brightness as a float value (ex. 1.5 = 50%% brighter)",
    )
    parser.add_argument(
        "-g",
        "--grayscale",
        action="store_true",
        help="convert to grayscale",
    )
    parser.add_argument(
        "-bl",
        "--blur",
        type=int,
        help="blur an image",
        nargs="?",
        const=3,
    )
    parser.add_argument(
        "-c",
        "--contrast",
        type=float,
        help="add contrast to an image",
        nargs="?",
        const=1,
    )
    parser.add_argument(
        "-mv",
        "--mirror_vertical",
        action="store_true",
        help="mirror across the y axis",
    )
    parser.add_argument(
        "-mh",
        "--mirror_horizontal",
        action="store_true",
        help="mirror across the x axis",
    )

    args = parser.parse_args()

    try:
        f = open(args.image_path, "rb")
        image = f.read()

        if args.verbose:
            print(args.verbose)
        output = ppm_to_pixels(image)

        if args.brightness:
            output = brightness(output, args.brightness)
        if args.grayscale:
            output = grayscale(output)
        if args.blur:
            output = box_blur(output, args.blur)
        if args.contrast:
            output = rgb_to_YCbCr(output)
            output = contrast(output, args.contrast)
            output = YCbCr_to_rgb(output)
        if args.mirror_horizontal:
            output = mirror_horizontal(output)
        if args.mirror_vertical:
            output = mirror_vertical(output)

        output = pixels_to_ppm(output)
        with open("out", "wb") as out:
            out.write(output)
    except FileNotFoundError:
        print(f"[Error] Image {args.image_path} does not exist")
