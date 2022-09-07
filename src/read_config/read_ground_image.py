import os

import cv2
import dill as pickle
import numpy as np
from preprocessing import cloud_mask
from processing.correlate_images import Keypoints
from time_and_shoot.sat_image import SatImage


def read_ground_image(pass_folder) -> SatImage:
    """
    returns a SatImage of the image we have on the ground
    """
    image_filename = os.path.join(pass_folder, "ground_image.tiff")
    # flip because the image is already in bgr
    default_image = SatImage(image=np.flip(cv2.imread(image_filename), axis=2))
    default_image.mask = cloud_mask.cloud_mask(default_image)
    return default_image


def read_ground_keypoints(filename) -> Keypoints:
    with open(filename, "rb") as file:
        ground_keypoints = Keypoints(from_hash=True, hash_object=pickle.load(file))
    print(f"loaded ground image Keypoints of image with shape {ground_keypoints.shape}")
    return ground_keypoints
