import cv2
import matplotlib.pyplot as plt
import numpy as np
from time_and_shoot.sat_image import SatImage


def blue_index(bgr):
    final_arr = 2 - (bgr[:, 1] + bgr[:, 2]) / bgr[:, 0]

    return np.nan_to_num(final_arr, nan=-1, posinf=-1, neginf=-1)


def water_index(bgr):
    g = int(bgr[1])
    r = int(bgr[2])
    return (g - r) / (g + r)


def compute_coastline(sat_image: SatImage) -> SatImage:
    """
    Computes the coastline of the image. Returns a black and white image mask, i.e. black is land, white is sea. The dtype is bool
    """
    image = sat_image.data
    height, width, _ = image.shape
    # filter_size = int(0.01 * (width + height) / 2)
    # img_blur = cv2.GaussianBlur(image, (filter_size, filter_size), 0)
    img_blur = image

    flat_data = img_blur.reshape((width * height, 3))
    # blue_values = np.array([blue_index(pixel) for pixel in flat_data])
    blue_values = blue_index(flat_data)
    # plt.hist(blue_values, bins=100, range=(-1, 1.5))
    # plt.show()

    in_sea = blue_values > 0.47
    in_sea = in_sea < 0.63
    in_sea = in_sea.reshape((height, width))
    # plt.imshow(in_sea)
    # plt.show()
    return SatImage(image=in_sea, mask=sat_image.mask)
