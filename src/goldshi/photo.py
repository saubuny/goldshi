from typing import List

type pixels = List[List[List[float]]]


# gaussian blur too complex for my tiny little brain
# outer ring of pixels are left unchanged
def box_blur(pixels: pixels, passes: int = 3) -> pixels:
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

                sum_red = (
                    pixels[row - 1][col + 1][0]
                    + pixels[row + 0][col + 1][0]
                    + pixels[row + 1][col + 1][0]
                    + pixels[row - 1][col + 0][0]
                    + pixels[row + 0][col + 0][0]
                    + pixels[row + 1][col + 0][0]
                    + pixels[row - 1][col - 1][0]
                    + pixels[row + 0][col - 1][0]
                    + pixels[row + 1][col - 1][0]
                )
                pixels[row][col][0] = sum_red / 9

                sum_green = (
                    pixels[row - 1][col + 1][1]
                    + pixels[row + 0][col + 1][1]
                    + pixels[row + 1][col + 1][1]
                    + pixels[row - 1][col + 0][1]
                    + pixels[row + 0][col + 0][1]
                    + pixels[row + 1][col + 0][1]
                    + pixels[row - 1][col - 1][1]
                    + pixels[row + 0][col - 1][1]
                    + pixels[row + 1][col - 1][1]
                )
                pixels[row][col][1] = sum_green / 9

                sum_blue = (
                    pixels[row - 1][col + 1][2]
                    + pixels[row + 0][col + 1][2]
                    + pixels[row + 1][col + 1][2]
                    + pixels[row - 1][col + 0][2]
                    + pixels[row + 0][col + 0][2]
                    + pixels[row + 1][col + 0][2]
                    + pixels[row - 1][col - 1][2]
                    + pixels[row + 0][col - 1][2]
                    + pixels[row + 1][col - 1][2]
                )
                pixels[row][col][2] = sum_blue / 9

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
