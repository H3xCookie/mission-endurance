import cv2
import numpy as np
from time_and_shoot.sat_image import SatImage


def mask_clouds(image: SatImage) -> SatImage:
    """
    mask the clouds. If the algorithm determines a pixel is of a cloud, it turns it all black
    """
    # TODO implement
    return image
