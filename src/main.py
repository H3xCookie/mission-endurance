import argparse
import os
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np

import cloud_mask
import compute_coastline
import correlate_images
import crop_field
import downlink
import precompute_coastline
import read_config_files
import read_ground_image
import setup_camera
import shoot
from correlate_images import Keypoints
from sat_image import SatImage


def preview_ground_image():
    gnd_image = cv2.imread("monkedir/ground_image_1_bgr.tiff")

    # already in rgb
    plt.imshow(np.clip(2 * gnd_image.astype(np.uint16), 0, 255))
    plt.show()


def sat_main(scale_factor=(5, 5)):
    """
    the main fn which runs on the satellite
    """
    # os.chdir("/work/mission-endurance/")
    parser = argparse.ArgumentParser(description="pass ")
    parser.add_argument("--field_filename", required=True)
    parser.add_argument("--ground_kpts", required=True)
    parser.add_argument("--time_filename", required=True)
    args = parser.parse_args()

    # ===================camera setup================================
    setup_camera.turn_on_camera()
    time_to_take_picture = read_config_files.time_of_photo(args.time_filename)

    # ===================satellite image manupulations==================
    sat_image = shoot.take_picture(time_to_take_picture)
    sat_image.mask = cloud_mask.cloud_mask(sat_image)
    sat_coastline = compute_coastline.compute_coastline(sat_image)
    sat_coastline_keypoints = correlate_images.get_keypoints(
        sat_coastline, scale_factor
    )

    # =====================ground image manupulations==================
    field_coords = read_config_files.field_coords(args.field_filename)
    print("load precomputed coastline Keypoints")
    ground_keypoints = read_ground_image.read_ground_keypoints(args.ground_kpts)

    # =====================aligning of the sat image==================
    print("compute homography")
    align_result = correlate_images.compute_transform_from_keypoints(
        sat_coastline_keypoints, ground_keypoints
    )
    homography, align_was_successful = align_result
    if not align_was_successful:
        print("cannot continue further, bad align")
        downlink.send_message_down("ALIGN UNSUCCESSFUL")
        sys.exit("ALIGN UNSUCCESSFUL")

    print("warp sat image to ground image")
    base_h, base_w = ground_keypoints.shape
    print("precomputed coastline h, w: ", base_h, base_w)
    sat_image = SatImage(
        image=cv2.warpPerspective(
            sat_image.data, homography, (base_h, base_w), flags=cv2.INTER_NEAREST
        )
    )

    # # =========================beam results back(for the sat)====================
    # # pass aligned image and coordinates to image recognition algorithm
    # poly_points = np.flip(field_coords, axis=1)
    # polygon = crop_field.Polygon(poly_points)

    # # code for the sat
    # only_field = crop_field.select_only_field(sat_image, polygon)
    # average_color = np.average(only_field.data, axis=(0, 1))
    # downlink.send_message_down(str(average_color))

    # ==================testing, remove before flight==================
    fig, ax = plt.subplots(1, 2)
    ground_image = read_ground_image.read_ground_image()
    for index, points in enumerate([field_coords, field_coords]):
        poly_points = np.flip(points, axis=1)
        polygon = crop_field.Polygon(poly_points)

        if index == 0:
            only_field = crop_field.select_only_field(ground_image, polygon)
        else:
            only_field = crop_field.select_only_field(sat_image, polygon)

        ax[index].imshow(
            np.clip(
                np.flip(only_field.data, axis=2).astype(np.float16) * 1.5, 0, 255
            ).astype(np.uint8)
        )

    plt.show()


if __name__ == "__main__":
    # preview_ground_image()
    scale_factor = (10, 10)
    precompute_coastline.precompute_coastline_keypoints(
        "config_files/2022-09-08T11_58_04", scale_factor
    )
    sat_main(scale_factor)
