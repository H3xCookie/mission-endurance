import cv2
from preprocessing import cloud_mask
from time_and_shoot.sat_image import SatImage


def read_coastline(pass_folder) -> SatImage:
    """
    returns a SatImage of the coastline which we have on the ground
    """
    image_filename = os.path.join("config_files", pass_folder, "ground_image.tiff")
    default_image = SatImage(image=cv2.imread(image_filename))
    default_image.mask = cloud_mask.cloud_mask(default_image)
    return default_image
