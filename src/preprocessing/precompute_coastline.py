import cv2
import dill as pickle
import matplotlib.pyplot as plt
import numpy as np
from processing import compute_coastline, correlate_images
from processing.correlate_images import Keypoints
from time_and_shoot.sat_image import SatImage

from preprocessing import cloud_mask


def precompute_coastline_keypoints():
    print("precompute Keypoints")
    base_image = cv2.imread("./monkedir/ground_image_1_rgb.tiff")

    final_image_data = compute_coastline.compute_coastline(SatImage(image=base_image))

    scale_factor = (2, 2)
    ground_keypoints = correlate_images.get_keypoints(final_image_data, scale_factor)
    print("Keypoints: ", len(ground_keypoints.kpts))
    output_with_keypoints = cv2.cvtColor(
        final_image_data.data.astype(np.uint8) * 255, cv2.COLOR_GRAY2RGB
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
    plt.imshow(output_with_keypoints)
    plt.show()
    new_filename = f"./monkedir/precomputed_scaled_{scale_factor[0]}_{scale_factor[1]}keypoingts.pkl"
    with open(
        new_filename,
        "wb",
    ) as file:
        pickle.dump(ground_keypoints.hashable(), file)
    print(f"Keypoints are saved in {new_filename}")


def load_precomputed_keypoints(filename) -> Keypoints:
    with open(filename, "rb") as file:
        ground_keypoints = Keypoints(from_hash=True, hash_object=pickle.load(file))
    print(f"loaded ground image Keypoints with shape {ground_keypoints.shape}")
    return ground_keypoints


def precompute_coastline():
    base_image = cv2.imread("./monkedir/stacked_rgb.tiff")

    cloud_filter = cloud_mask.cloud_mask(SatImage(image=base_image))

    final_image_data = compute_coastline.compute_coastline(SatImage(image=base_image))
    final_image_data = final_image_data.data.astype(np.uint8) * 255
    # TODO create a better compression for the computed coastline
    cv2.imwrite("./monkedir/precomputed_coastline_rgb_sat.tiff", final_image_data)


def load_precomputed_coastline(filename) -> SatImage:
    return SatImage(image=cv2.cvtColor(cv2.imread(filename) * 255, cv2.COLOR_BGR2GRAY))
