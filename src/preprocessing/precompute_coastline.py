import os

import cv2
import dill as pickle
import matplotlib.pyplot as plt
import numpy as np

from preprocessing import cloud_mask
from processing import compute_coastline, correlate_images
from processing.correlate_images import Keypoints
from read_config import read_ground_image
from time_and_shoot.sat_image import SatImage


def precompute_coastline_keypoints(pass_folder, scale_factor=(5, 5)):
    ground_coastline = read_ground_image.read_ground_image(pass_folder)
    ground_coastline = compute_coastline.compute_coastline(ground_coastline)
    ground_keypoints = correlate_images.get_keypoints(ground_coastline, scale_factor)
    print("Keypoints: ", len(ground_keypoints.kpts))
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
    # new_filename = f"./monkedir/precomputed_scaled_{scale_factor[0]}_{scale_factor[1]}keypoints.pkl"
    keypoint_filename = os.path.join(
        pass_folder,
        f"ground_keypoints_{scale_factor[0]:.0f}_{scale_factor[1]:.0f}.pkl",
    )
    with open(
        keypoint_filename,
        "wb",
    ) as file:
        pickle.dump(ground_keypoints.hashable(), file)
    print(f"Keypoints are saved in {keypoint_filename}")
