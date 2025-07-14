from typing import List

# The functions in here would be good to unit test.


def ppm_to_pixels(image: bytes) -> List[List[List[float]]]:
    pixels = [[[]]]  # this looks so dumb LOL
    s = image.split()
    x, y = int(s[1]), int(s[2])

    offset = 4  # this is where pixels start
    for i in range(offset, len(s), 3):
        for j in range(3):
            # put in the pixels array !
            print(int(s[i + j]), end=" ")
        print()

    # x, y = float(s[1]) / 255, float(s[2]) / 255

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
