from typing import List


def ppm_to_pixels(image: bytes) -> List[List[List[float]]]:
    s = image.split()
    pixels = [
        [[0.0 for _ in range(3)] for _ in range(int(s[1]))] for _ in range(int(s[2]))
    ]  # [row][column][channel]

    offset = 4  # pixel start
    row = 0
    col = 0
    for i in range(offset, len(s), 3):
        for j in range(3):
            pixels[row][col][j] = float(s[i + j]) / 255

        col += 1
        if col % int(s[1]) == 0:
            col = 0
            row += 1

    return pixels


def pixels_to_ppm(pixels: List[List[List[float]]]) -> bytes: ...


# Not a very useful function :<
def create_test_ppm() -> None:
    f = open("out", "w")
    f.writelines(
        [
            "P3\n",
            "3 2\n",
            "255\n",
            "255   0   0\n",
            "  0 255   0\n",
            "  0   0 255\n",
            "255 255   0\n",
            "255 255 255\n",
            "  0   0   0\n",
        ]
    )
