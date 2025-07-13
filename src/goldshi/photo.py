# Converts p3 ppm image into a 2d array of pixels to manipulate
def ppm_to_pixels(): ...


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
