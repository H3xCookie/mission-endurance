import argparse
import os
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np

from communications import downlink
from preprocessing import cloud_mask, precompute_coastline
from processing import compute_coastline, correlate_images, crop_field
from processing.correlate_images import Keypoints
from read_config import read_config_files
from time_and_shoot import setup_camera, shoot
from time_and_shoot.sat_image import SatImage


def preview_ground_image():
    gnd_image = cv2.imread("monkedir/ground_image_1_bgr.tiff")

    # already in rgb
    plt.imshow(np.clip(2 * gnd_image.astype(np.uint16), 0, 255))
    plt.show()


def sat_main(scale_factor=(5, 5)):
    """
    the main fn which runs on the satellite. fiedl coords must
    be in the form (x, y), and be in counter-clockwise direction in the coordinate system of the image(x right, y down).
    """
    # os.chdir("/work/mission-endurance/")
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
    sat_coastline_keypoints = correlate_images.get_keypoints(
        sat_coastline, scale_factor
    )
    # x then y coordinate, need to flip them later so y is first, then x
    #
    # good_fields = [
    #     [[2031, 1106], [2107, 1097], [2093, 1008], [2023, 1034]],
    #     [[2031, 1106], [2107, 1097], [2093, 1008], [2023, 1034]],
    # ]
    # bad_fields = [
    #     [[2057, 1214], [2127, 1216], [2111, 1124], [2056, 1123]],
    #     [[2057, 1214], [2127, 1216], [2111, 1124], [2056, 1123]],
    # ]
    field_coords = read_config_files.field_coords("pass_1")

    print("load precomputed coastline Keypoints")
    ground_keypoints = precompute_coastline.load_precomputed_keypoints(
        args.ground_keypoints
    )

    # compute and apply homography to the original sat image
    print("compute homography")
    align_result = correlate_images.compute_transform_from_keypoints(
        sat_coastline_keypoints, ground_keypoints
    )
    homography, align_was_successful = align_result
    if not align_was_successful:
        print("cannot continue further")
        downlink.send_message_down(f"ALIGN UNSUCCESSFUL")
        sys.exit("ALIGN UNSUCCESSFUL")

    print("warp sat image to ground image")
    base_h, base_w = ground_keypoints.shape
    print("precomputed coastline h, w: ", base_h, base_w)
    sat_image = SatImage(
        image=cv2.warpPerspective(
            sat_image.data, homography, (base_h, base_w), flags=cv2.INTER_NEAREST
        )
    )

    fig, ax = plt.subplots(1, 2)
    ground_image = SatImage(image=cv2.imread("monkedir/ground_image_1_bgr.tiff"))
    ground_image.data = np.flip(ground_image.data, axis=2)
    for index, points in enumerate([field_coords]):
        # pass aligned image and coordinates to image recognition algorithm
        poly_points = np.flip(points, axis=1)
        polygon = crop_field.Polygon(poly_points)

        only_field = crop_field.select_only_field(sat_image, polygon)
        average_color = np.average(only_field.data, axis=(0, 1))
        # send data back to earth
        downlink.send_message_down(f"{average_color}")
        # print("crop field")

        # if index == 0:
        #     only_field = crop_field.select_only_field(ground_image, polygon)
        # else:
        #     only_field = crop_field.select_only_field(sat_image, polygon)

        # # compute the Green index of the field
        # print("compute index")
        # green_index = indeces.green_index(only_field)

        # is_planted = make_decision.is_field_planted(green_index)
        # # downlink.send_message_down(f"{green_index}: {is_planted}")
        # ax[index].imshow(
        #     np.clip(
        #         np.flip(only_field.data, axis=2).astype(np.float16) * 1.5, 0, 255
        #     ).astype(np.uint8)
        # )
        # ax[index].title.set_text(f"green coeff {green_index: .2f}: {is_planted}")

    plt.show()


if __name__ == "__main__":
    # preview_ground_image()
    scale_factor = (10, 10)
    precompute_coastline.precompute_coastline_keypoints(scale_factor)
    sat_main(scale_factor)
