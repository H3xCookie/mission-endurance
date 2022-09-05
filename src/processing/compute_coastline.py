import cv2
import matplotlib.pyplot as plt
import numpy as np
from time_and_shoot.sat_image import SatImage


def blue_index(bgr) -> np.ndarray:
    new_color = bgr.astype(np.float16)
    final_arr = new_color[:, 0] / (new_color[:, 2] + new_color[:, 1])

    return final_arr
    # return np.nan_to_num(final_arr, nan=-1, posinf=-1, neginf=-1).astype(np.float16)


def water_index(bgr):
    g = int(bgr[1])
    r = int(bgr[2])
    return (g - r) / (g + r)


def grayscale_coastline(sat_image: SatImage) -> SatImage:
    """
    Computes the coastline of the image. Returns a black and white image mask, i.e. black is land, white is sea. The dtype is bool
    """
    image = sat_image.data
    height, width, _ = image.shape

    blue_values = blue_index(image.reshape((height * width, 3)))
    max_value = np.quantile(blue_values, 0.98)
    blue_values = np.clip(blue_values.astype(np.float16) * 254.0 / max_value, 0, 255)
    blue_values = blue_values.astype(np.uint8)
    filter_size = max(5, int(int(0.01 * height) / 2) * 2 + 1)
    print(f"filter size {filter_size}")

    blurred_coastline = cv2.GaussianBlur(
        blue_values.reshape((height, width)),
        (filter_size, filter_size),
        0,
    )

    _, blurred_coastline = cv2.threshold(
        blurred_coastline, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    blurred_coastline = blurred_coastline.astype(np.uint8) * 255
    filter_size = max(5, int(int(0.002 * height) / 2) * 2 + 1)
    blurred_coastline = cv2.GaussianBlur(
        blurred_coastline,
        (filter_size, filter_size),
        0,
    )
    print("blurred_coastline")
    plt.imshow(blurred_coastline)
    plt.show()

    return SatImage(image=blurred_coastline, mask=sat_image.mask)


def compute_coastline(sat_image: SatImage) -> SatImage:
    """
    Computes the coastline of the image. Returns a black and white image mask, i.e. black is land, white is sea. The dtype is bool
    """
    image = sat_image.data
    height, width, _ = image.shape

    blue_values = blue_index(image.reshape((height * width, 3)))
    max_value = np.quantile(blue_values, 0.98)
    blue_values = np.clip(blue_values.astype(np.float16) * 254.0 / max_value, 0, 255)
    blue_values = blue_values.astype(np.uint8)

    filter_size = max(5, int(int(0.01 * height) / 2) * 2 + 1)
    print(filter_size)
    blueness_image = cv2.GaussianBlur(
        blue_values.reshape((height, width)),
        (filter_size, filter_size),
        0,
    )
    _, coastline_mask = cv2.threshold(
        blueness_image, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    coastline_mask = coastline_mask.astype(bool)

    coastline_mask = ~coastline_mask
    # plt.imshow(coastline_mask)
    # plt.show()
    return SatImage(image=coastline_mask, mask=sat_image.mask)
