from typing import List


# Linear approximation of gamma and perceptual luminance corrected
def grayscale_pixels(pixels: List[List[List[float]]]) -> List[List[List[float]]]:
    for row in pixels:
        for col in row:
            average = (col[0] * 0.299) + (col[1] * 0.587) + (col[2] * 0.114)
            col[0] = average
            col[1] = average
            col[2] = average
    return pixels


def ppm_to_pixels(image: bytes) -> List[List[List[float]]]:
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


def pixels_to_ppm(pixels: List[List[List[float]]]) -> bytes:
    image = f"P3\n{len(pixels[0])} {len(pixels)}\n255\n"

    for row in pixels:
        for col in row:
            for ch in col:
                image += str(int(ch * 255)) + " "
        image += "\n"

    return image.encode("utf-8")
