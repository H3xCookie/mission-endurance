from time_and_shoot.sat_image import SatImage
from processing import compute_coastline
import cv2
import numpy as np


def precompute_coastline():
    base_image = cv2.imread("./monkedir/base_image_example.tiff")
    final_image_data = compute_coastline.compute_coastline(SatImage(image=base_image))
    final_image_data = final_image_data.data.astype(np.uint8) * 255
    # TODO create a better compression for the computed coastline
    cv2.imwrite("./monkedir/precomputed_coastline.tiff", final_image_data)


def load_precomputed_coastline(filename) -> SatImage:
    return SatImage(image=cv2.cvtColor(cv2.imread(filename) * 255, cv2.COLOR_BGR2GRAY))
