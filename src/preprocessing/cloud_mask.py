import cv2
import matplotlib.pyplot as plt
import numpy as np
from time_and_shoot.sat_image import SatImage


def cloud_mask(image: SatImage) -> np.ndarray:
    """
    mask the clouds. returns a np.ndarray from bools, true is usable data, false is cloud
    """
    return np.full(image.data.shape[:2], True)
