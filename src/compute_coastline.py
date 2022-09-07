import cv2
import matplotlib.pyplot as plt
import numpy as np

from sat_image import SatImage


def blue_index(bgr: np.ndarray) -> np.ndarray:
    """
    receives the data of the SatImage as a np.ndarray and calculates a blueness value
    """
    new_color = bgr.astype(np.float16)
    final_arr = new_color[:, :, 0] / (new_color[:, :, 2] + new_color[:, :, 1] + 0.00001)

    return final_arr


def compute_coastline(sat_image: SatImage) -> SatImage:
    """
    Computes the coastline of the image. Returns a black and white image mask, i.e. black is land, white is sea. The dtype is bool
    """
    image = sat_image.data
    height, width = image.shape[:2]

    blue_values = blue_index(image)
    max_value = np.quantile(blue_values, 0.98)
    blue_values = np.clip(blue_values * 254.0 / max_value, 0, 255)
    blue_values = blue_values.astype(np.uint8)

    filter_size = max(5, int(int(0.01 * height) / 2) * 2 + 1)
    blue_values = cv2.GaussianBlur(
        blue_values,
        (filter_size, filter_size),
        0,
    )
    _, coastline_mask = cv2.threshold(
        blue_values, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    coastline_mask = coastline_mask.astype(bool)

    return SatImage(image=coastline_mask, mask=sat_image.mask)
