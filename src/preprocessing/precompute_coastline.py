import cv2
import dill as pickle
import numpy as np
from processing import compute_coastline, correlate_images
from processing.correlate_images import Keypoints
from time_and_shoot.sat_image import SatImage

from preprocessing import cloud_mask


def precompute_coastline():
    base_image = cv2.imread("./monkedir/stacked_rgb.tiff")

    cloud_filter = cloud_mask.cloud_mask(SatImage(image=base_image))

    final_image_data = compute_coastline.compute_coastline(SatImage(image=base_image))
    final_image_data = final_image_data.data.astype(np.uint8) * 255
    # TODO create a better compression for the computed coastline
    cv2.imwrite("./monkedir/precomputed_coastline_rgb_sat.tiff", final_image_data)


def precompute_coastline_keypoints():
    print("precompute Keypoints")
    base_image = cv2.imread("./monkedir/stacked_rgb.tiff")

    # TODO use the cloud mask
    # cloud_filter = cloud_mask.cloud_mask(SatImage(image=base_image))

    final_image_data = compute_coastline.compute_coastline(SatImage(image=base_image))
    ground_keypoints = correlate_images.get_keypoints(final_image_data)
    with open("./monkedir/precomputed_keypoingts.pkl", "wb") as file:
        pickle.dump(ground_keypoints.hashable(), file)
    print("Keypoints are saved in ./monkedir/precomputed_keypoingts.pkl")


def load_precomputed_coastline(filename) -> SatImage:
    return SatImage(image=cv2.cvtColor(cv2.imread(filename) * 255, cv2.COLOR_BGR2GRAY))


def load_precomputed_keypoints(filename) -> Keypoints:
    with open(filename, "rb") as file:
        ground_keypoints = Keypoints(from_hash=True, hash_object=pickle.load(file))
    print(f"loaded ground image Keypoints with shape {ground_keypoints.shape}")
    return ground_keypoints
