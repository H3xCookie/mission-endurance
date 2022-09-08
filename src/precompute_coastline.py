import os

import cv2
import dill as pickle
# import matplotlib.pyplot as plt
import numpy as np

import compute_coastline
import correlate_images
import read_ground_image
from correlate_images import Keypoints
from sat_image import SatImage


def precompute_coastline_keypoints(scale_factor=(5, 5)):
    ground_coastline = read_ground_image.read_ground_image()
    ground_coastline = compute_coastline.compute_coastline(ground_coastline)
    ground_keypoints = correlate_images.get_keypoints(ground_coastline, scale_factor)
    print("Keypoints: ", len(ground_keypoints.kpts))
    # satellite >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # ===============================================================
    output_with_keypoints = cv2.cvtColor(
        ground_coastline.data.astype(np.uint8) * 255, cv2.COLOR_GRAY2RGB
    )
    for kp in ground_keypoints.kpts:
        x, y = kp.pt
        cv2.circle(
            output_with_keypoints,
            (int(x), int(y)),
            15,
            color=(255, 0, 0),
            thickness=-1,
        )
    print("output_with_keypoints")
    plt.imshow(output_with_keypoints)
    plt.show()
    # testing <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    keypoint_filename = (
        f"ground_keypoints_{scale_factor[0]:.0f}_{scale_factor[1]:.0f}.pkl"
    )
    with open(
        keypoint_filename,
        "wb",
    ) as file:
        pickle.dump(ground_keypoints.hashable(), file)
