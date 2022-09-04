import sys
import cv2
import numpy as np
from processing import compute_coastline
from time_and_shoot.sat_image import SatImage

from preprocessing import cloud_mask


def precompute_coastline():
    base_image = cv2.imread("./monkedir/stacked_rgb.tiff")

    cloud_filter = cloud_mask.cloud_mask(SatImage(image=base_image))

    final_image_data = compute_coastline.compute_coastline(SatImage(image=base_image))
    final_image_data = final_image_data.data.astype(np.uint8) * 255
    # TODO create a better compression for the computed coastline
    cv2.imwrite("./monkedir/precomputed_coastline_rgb_sat.tiff", final_image_data)


def load_precomputed_coastline(filename) -> SatImage:
    return SatImage(image=cv2.cvtColor(cv2.imread(filename) * 255, cv2.COLOR_BGR2GRAY))


