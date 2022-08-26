import cv2
import matplotlib.pyplot as plt
import numpy as np


def blue_index(bgr):
    return (2 * int(bgr[0]) - int(bgr[1]) - int(bgr[2])) / bgr[0]


def compute_coastline(image_filename, csv=False) -> np.ndarray:
    """
    Computes the coastline of the image. If csv=False, returns a black and white image mask, i.e. black is coastline, white is not
    """
    # TODO make it better
    image: np.ndarray = cv2.imread(image_filename)
    height, width, _ = image.shape
    filter_size = int(0.01 * (width + height) / 2)
    img_blur = cv2.GaussianBlur(image, (filter_size, filter_size), 0)

    flat_data = img_blur.reshape((width * height, 3))
    blue_values = np.array([blue_index(pixel) for pixel in flat_data])

    in_sea = blue_values > 0.6
    border_initial_image = in_sea.reshape((height, width))
    return border_initial_image
