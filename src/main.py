import argparse

import cv2
import matplotlib.pyplot as plt
import numpy as np

from communications import downlink
from image_analysis import indeces, make_decision
from preprocessing import cloud_mask, precompute_coastline
from processing import compute_coastline, correlate_images, crop_field
from processing.correlate_images import Keypoints
from time_and_shoot import setup_camera, shoot
from time_and_shoot.sat_image import SatImage


def sat_main():
    """
    the main fn which runs on the satellite. fiedl coords must
    be in the form (x, y), and be in counter-clockwise direction in the coordinate system of the image(x right, y down).
    """
    parser = argparse.ArgumentParser(description="Pass precomputed coastline")
    parser.add_argument("--ground_keypoints", required=True)
    args = parser.parse_args()

    print("take picture")
    setup_camera.turn_on_camera()
    time_to_take_picture = "2022:09:03,12:00:00,000"
    sat_image = shoot.take_picture(time_to_take_picture)
    height, width = sat_image.data.shape[:2]

    print("sat image h, w: ", height, width)
    # add mask attribute to the image
    print("compute cloud mask of picture")
    # sat_image.mask = cloud_mask.cloud_mask(sat_image)
    print("compute coastline and Keypoints of picture")
    sat_coastline = compute_coastline.compute_coastline(sat_image)
    scale_factor = (10, 10)
    sat_coastline_keypoints = correlate_images.get_keypoints(
        sat_coastline, scale_factor
    )
    # x then y coordinate, need to flip them later so y is first, then x
    good_fields = [
        [[2100, 450], [2100, 1000], [3000, 1000], [3000, 200]],
        [[2100, 450], [2100, 1000], [3000, 1000], [3000, 200]],
    ]
    bad_fields = [
        [[2100, 450], [2100, 1000], [3000, 1000], [3000, 200]],
        [[2100, 450], [2100, 1000], [3000, 1000], [3000, 200]],
    ]

    print("load precomputed coastline Keypoints")
    ground_keypoints = precompute_coastline.load_precomputed_keypoints(
        args.ground_keypoints
    )

    # compute and apply homography to the original sat image
    print("compute homography")
    homography = correlate_images.compute_transform_from_keypoints(
        sat_coastline_keypoints,
        ground_keypoints,
        sat_image,
        SatImage(image=cv2.imread("monkedir/ground_image_1_rgb.tiff")),
    )

    print("warp sat image to ground image")
    base_h, base_w = ground_keypoints.shape
    print("precomputed coastline h, w: ", base_h, base_w)
    sat_image = SatImage(
        image=cv2.warpPerspective(
            sat_image.data, homography, (base_h, base_w), flags=cv2.INTER_NEAREST
        )
    )
    fig, ax = plt.subplots(2, 2)
    for dataset_index, dataset in enumerate([good_fields, bad_fields]):
        for index, points in enumerate(dataset):
            print(points)
            # pass aligned image and coordinates to image recognition algorithm
            poly_points = np.flip(np.array(points).reshape((len(points), 2)), axis=1)
            polygon = crop_field.Polygon(poly_points)

            print("crop field")
            only_field = crop_field.select_only_field(sat_image, polygon)
            # compute the Green index of the field
            print("compute index")
            green_index = indeces.green_index(only_field)

            is_planted = make_decision.is_field_planted(green_index)
            # downlink.send_message_down(f"{green_index}: {is_planted}")
            ax[dataset_index][index].imshow(np.flip(only_field.data, axis=2))
            ax[dataset_index][index].title.set_text(
                f"green coeff {green_index: .2f}: {is_planted}"
            )

    plt.show()


if __name__ == "__main__":
    # sat_main()
    # print("main of main")
    precompute_coastline.precompute_coastline_keypoints()
