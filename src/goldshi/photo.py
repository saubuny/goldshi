from typing import List

from goldshi.helper import clamp

type pixels = List[List[List[float]]]

VERBOSE = True


# gaussian blur too complex for my tiny little brain
# outer ring of pixels are left unchanged
# slow as FUCK
def box_blur(pixels: pixels, passes: int = 3) -> pixels:
    for p in range(passes):
        if VERBOSE:
            print(f"[INFO] Starting blur pass {p}")
        for row in range(len(pixels)):
            for col in range(len(pixels[row])):
                if (
                    row < 1
                    or col < 1
                    or row + 1 >= len(pixels)
                    or col + 1 >= len(pixels[col])
                ):
                    continue

                for c in range(3):
                    sum = (
                        pixels[row - 1][col + 1][c]
                        + pixels[row + 0][col + 1][c]
                        + pixels[row + 1][col + 1][c]
                        + pixels[row - 1][col + 0][c]
                        + pixels[row + 0][col + 0][c]
                        + pixels[row + 1][col + 0][c]
                        + pixels[row - 1][col - 1][c]
                        + pixels[row + 0][col - 1][c]
                        + pixels[row + 1][col - 1][c]
                    )
                    pixels[row][col][c] = sum / 9
    return pixels


# Linear approximation of gamma and perceptual luminance corrected
def grayscale(pixels: pixels) -> pixels:
    for row in pixels:
        for col in row:
            average = (col[0] * 0.299) + (col[1] * 0.587) + (col[2] * 0.114)
            col[0] = average
            col[1] = average
            col[2] = average
    return pixels


def brightness(pixels: pixels, change: float) -> pixels:
    for row in pixels:
        for col in row:
            col[0] = clamp(col[0] * change, 0, 1)
            col[1] = clamp(col[1] * change, 0, 1)
            col[2] = clamp(col[2] * change, 0, 1)
    return pixels


# histogram equalization
def contrast(pixels: pixels) -> pixels: ...


def rgb_to_YCbCr(pixels: pixels) -> pixels: ...


def ppm_to_pixels(image: bytes) -> pixels:
    s = image.split()
    pixels = [
        [[0.0 for _ in range(3)] for _ in range(int(s[1]))] for _ in range(int(s[2]))
    ]  # [row][column][channel]

    if s[0] != b"P3":
        raise Exception("Only the P3 format is supported")

    offset = 4  # pixel start
    row = 0
    col = 0
    for i in range(offset, len(s), 3):
        for j in range(3):
            if int(s[i + j]) < 0 or int(s[i + j]) > int(s[3]):  # invalid rgb value
                raise Exception("Invalid PPM file given")

            pixels[row][col][j] = float(s[i + j]) / 255

        col += 1
        if col % int(s[1]) == 0:
            col = 0
            row += 1

    return pixels


def pixels_to_ppm(pixels: pixels) -> bytes:
    image = f"P3\n{len(pixels[0])} {len(pixels)}\n255\n"

    for row in pixels:
        for col in row:
            for ch in col:
                image += str(int(ch * 255)) + " "
        image += "\n"

    return image.encode("utf-8")
