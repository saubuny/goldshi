from types import FunctionType
from typing import List
from math import ceil, floor

type Pixels = List[List[List[float]]]


# confusing, but row  is y and col is x
def new_Pixels(row: int, col: int) -> Pixels:
    return [
        [[0.0 for _ in range(3)] for _ in range(int(col))] for _ in range(int(row))
    ]  # [row][column][channel]


def clamp(n: float, min: float, max: float) -> float:
    if n > max:
        return max
    if n < min:
        return min
    return n


# gaussian blur too complex for my tiny little brain
# outer ring of pixels are left unchanged
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


# percentile stretching
def contrast(pixels: Pixels, factor: float = 1) -> Pixels:
    y_values = [col[0] for row in pixels for col in row]
    min = y_values[percentile(2, y_values)]
    max = y_values[percentile(98, y_values)]

    for row in range(len(pixels)):
        for col in range(len(pixels[row])):
            pixels[row][col][0] = (pixels[row][col][0] - min) / (max - min) * factor

    return pixels


def percentile(percentile: int, pixels: list) -> int:
    pixels.sort()
    return int((percentile / 100) * (len(pixels) - 1))


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

            new_pixels[row][col][0] = clamp(y, 0, 1)
            new_pixels[row][col][1] = clamp(cb, 127.5, 128.5)
            new_pixels[row][col][2] = clamp(cr, 127.5, 128.5)
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

            new_pixels[row][col][0] = clamp(r, 0, 1)
            new_pixels[row][col][1] = clamp(g, 0, 1)
            new_pixels[row][col][2] = clamp(b, 0, 1)
    return new_pixels


def ppm_to_pixels(image: bytes) -> Pixels:
    s = image.split()
    pixels = new_Pixels(int(s[2]), int(s[1]))

    if s[0] != b"P3":
        raise Exception("Only the P3 format is supported")

    offset = 4  # pixel start
    row = 0
    col = 0
    for i in range(offset, len(s), 3):
        for j in range(3):
            if int(s[i + j]) < 0 or int(s[i + j]) > int(s[3]):
                raise Exception("Invalid RGB values in PPM file given")

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
                if ch < 0 or ch > 255:
                    raise Exception("Invalid RGB values")
                image += str(int(ch * 255)) + " "
        image += "\n"

    return image.encode("utf-8")


# duplicate a pixel if the new value of adding scale - 1 to a growing value crosses a new integer
# ex w/ 1.75 scale (75% increase)
# 0 - 1.50 [2 * (scale-1)] dup
# 1 - 2.25 dup
# 2 - 3.00 dup
# 3 - 3.75 don't dup
# 4 - 4.50 dup
# 5 - 5.25 dup
# 6 - 6.00 dup
# 7 - 6.75 don't dup
# i don't know how i came up with this but it somehow works
# TODO: combine resize_y and resize_x into one function somehow
def resize_y(pixels: Pixels, y: int) -> Pixels:
    new_pixels = new_Pixels(y, len(pixels[0]))
    scale_y = y / len(pixels)

    if scale_y <= 0:
        raise Exception("Can not scale to a negative number")

    def copy_row(new_row: int, row: int) -> int:
        for col in range(len(pixels[0])):
            for ch in range(3):
                new_pixels[new_row][col][ch] = pixels[row][col][ch]
        return new_row + 1

    new_row = 0
    prev_dup = 0
    dup = (scale_y - 1) * 2
    for row in range(len(pixels)):
        if scale_y < 1 and ceil(prev_dup) != ceil(dup):
            prev_dup = dup
            dup += scale_y - 1
            continue
        elif floor(prev_dup) != floor(dup):
            for _ in range(floor(dup) - floor(prev_dup)):
                new_row = copy_row(new_row, row)
        if new_row < y:  # avoid index error
            new_row = copy_row(new_row, row)
        prev_dup = dup
        dup += scale_y - 1
    return new_pixels


# lots of repeated code, but must be in own function
def resize_x(pixels: Pixels, x: int) -> Pixels:
    new_pixels = new_Pixels(len(pixels), x)
    scale_x = x / len(pixels[0])

    if scale_x <= 0:
        raise Exception("Can not scale to a non-positive number")

    new_col = 0
    inc = scale_x - 1
    dup = inc
    prev_dup = 0
    for col in range(len(pixels[0])):
        dup += inc
        if scale_x < 1:
            if ceil(prev_dup) != ceil(dup):
                prev_dup = dup
                continue
        else:
            if floor(prev_dup) != floor(dup):
                for row in range(len(pixels)):
                    for ch in range(3):
                        new_pixels[row][new_col][ch] = pixels[row][col][ch]
                new_col += 1
        for row in range(len(pixels)):
            for ch in range(3):
                new_pixels[row][new_col][ch] = pixels[row][col][ch]
        new_col += 1
        prev_dup = dup
    return new_pixels


def mirror(pixels: Pixels, vert: bool = False) -> Pixels: ...
