import os

import cv2
from time_and_shoot.sat_image import SatImage

from preprocessing import cloud_mask


def read_ground_image(pass_folder) -> SatImage:
    """
    returns a SatImage of the image we have on the ground
    """
    image_filename = os.path.join("config_files", pass_folder, "ground_image.tiff")
    default_image = SatImage(image=cv2.imread(image_filename))
    default_image.mask = cloud_mask.cloud_mask(default_image)
    return default_image
