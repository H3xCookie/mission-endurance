import cv2
import matplotlib.pyplot as plt
import numpy as np

from time_and_shoot.sat_image import SatImage


def blue_index(bgr):
    return (2 * int(bgr[0]) - int(bgr[1]) - int(bgr[2])) / bgr[0]


def water_index(bgr):
    g = int(bgr[1])
    r = int(bgr[2])
    return (g - r) / (g + r)


def compute_coastline(sat_image: SatImage, csv=False) -> SatImage:
    """
    Computes the coastline of the image. If csv=False, returns a black and white image mask, i.e. black is land, white is sea. The dtype is bool
    """
    # TODO make it better
    image = sat_image.data
    height, width, _ = image.shape
    filter_size = int(0.01 * (width + height) / 2)
    img_blur = cv2.GaussianBlur(image, (filter_size, filter_size), 0)

    flat_data = img_blur.reshape((width * height, 3))
    blue_values = np.array([blue_index(pixel) for pixel in flat_data])
    # plt.hist(blue_values, bins=100)
    # plt.show()

    in_sea = blue_values > 0.6
    border_initial_image = in_sea.reshape((height, width))
    print(border_initial_image.dtype)
    return SatImage(image=border_initial_image)
