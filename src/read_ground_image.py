import os

import cv2
import dill as pickle
import numpy as np

import cloud_mask
from correlate_images import Keypoints
from sat_image import SatImage


# satellite >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ===================================================================
def read_ground_image() -> SatImage:
    """
    returns a SatImage of the image we have on the ground. THIS FN SHOULD NOT BE IN SPACE
    """
    image_filename = os.path.join("stacked_bgr_namibia.tif")
    # flip because the image is already in bgr
    default_image = SatImage(image=np.flip(cv2.imread(image_filename), axis=2))
    default_image.mask = cloud_mask.cloud_mask(default_image)
    return default_image


# testing <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


def read_ground_keypoints(filename) -> Keypoints:
    with open(filename, "rb") as file:
        ground_keypoints = Keypoints(from_hash=True, hash_object=pickle.load(file))
    return ground_keypoints
