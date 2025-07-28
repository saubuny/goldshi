from typing import List

from goldshi.helper import clamp

# probably better to make a stricter format where the innermost list is a named tuple for rgb/ycbcr
type Pixels = List[List[List[float]]]


def new_Pixels(row, col) -> Pixels:
    return [
        [[0.0 for _ in range(3)] for _ in range(int(col))] for _ in range(int(row))
    ]  # [row][column][channel]


# gaussian blur too complex for my tiny little brain
# outer ring of pixels are left unchanged
# slow as FUCK
def box_blur(pixels: Pixels, passes: int = 3) -> Pixels:
    for _ in range(passes):
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
def grayscale(pixels: Pixels) -> Pixels:
    for row in pixels:
        for col in row:
            average = (col[0] * 0.299) + (col[1] * 0.587) + (col[2] * 0.114)
            col[0] = average
            col[1] = average
            col[2] = average
    return pixels


def brightness(pixels: Pixels, change: float) -> Pixels:
    for row in pixels:
        for col in row:
            col[0] = clamp(col[0] * change, 0, 1)
            col[1] = clamp(col[1] * change, 0, 1)
            col[2] = clamp(col[2] * change, 0, 1)
    return pixels


# min-max stretching, as i'm literally too stupid to understand histogram equilization right now
# DOES NOT WORK
def contrast(pixels: Pixels) -> Pixels:
    min = pixels[0][0][0]
    max = pixels[0][0][0]
    for row in pixels:
        for col in row:
            if col[0] < min:
                min = col[0]
            if col[0] > max:
                max = col[0]

    for row in range(len(pixels)):
        for col in range(len(pixels[row])):
            pixels[row][col][0] = (pixels[row][col][0] - min) / (max - min)

    return pixels


# https://en.wikipedia.org/wiki/YCbCr#JPEG_conversion
def rgb_to_YCbCr(pixels: Pixels) -> Pixels:
    new_pixels = new_Pixels(len(pixels), len(pixels[0]))
    for row in range(len(pixels)):
        for col in range(len(pixels[row])):
            r = pixels[row][col][0]
            g = pixels[row][col][1]
            b = pixels[row][col][2]

            y = (0.299 * r) + (0.587 * g) + (0.114 * b)
            cb = 128 - (0.168736 * r) - (0.331264 * g) + (0.5 * b)
            cr = 128 + (0.5 * r) - (0.418688 * g) - (0.081312 * b)

            new_pixels[row][col][0] = y
            new_pixels[row][col][1] = cb
            new_pixels[row][col][2] = cr
    return new_pixels


def YCbCr_to_rgb(pixels: Pixels) -> Pixels:
    new_pixels = new_Pixels(len(pixels), len(pixels[0]))
    for row in range(len(pixels)):
        for col in range(len(pixels[row])):
            y = pixels[row][col][0]
            cb = pixels[row][col][1]
            cr = pixels[row][col][2]

            r = y + 1.402 * (cr - 128)
            g = y - 0.344136 * (cb - 128) - 0.714136 * (cr - 128)
            b = y + 1.772 * (cb - 128)

            new_pixels[row][col][0] = r
            new_pixels[row][col][1] = g
            new_pixels[row][col][2] = b
    return new_pixels


def ppm_to_pixels(image: bytes) -> Pixels:
    s = image.split()
    pixels = new_Pixels(s[2], s[1])

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


def pixels_to_ppm(pixels: Pixels) -> bytes:
    image = f"P3\n{len(pixels[0])} {len(pixels)}\n255\n"

    for row in pixels:
        for col in row:
            for ch in col:
                image += str(int(ch * 255)) + " "
        image += "\n"

    return image.encode("utf-8")
