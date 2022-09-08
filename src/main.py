import argparse
import os
import sys
from subprocess import run

import cv2
# import matplotlib.pyplot as plt
import numpy as np

import cloud_mask
import compute_coastline
import correlate_images
import crop_field
import downlink
import read_config_files
import read_ground_image
import shoot
from correlate_images import Keypoints
from sat_image import SatImage


def sat_main(scale_factor=(5, 5)):
    """
    the main fn which runs on the satellite
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--field_filename", required=True)
    parser.add_argument("--ground_kpts", required=True)
    parser.add_argument("--time_filename", required=True)
    parser.add_argument("--job_path", required=True)
    args = parser.parse_args()

    # ===================camera setup================================
    time_to_take_picture = read_config_files.time_of_photo(args.time_filename)

    # ===================satellite image manupulations==================
    sat_image = shoot.take_picture(args.job_path, time_to_take_picture)
    sat_image.mask = cloud_mask.cloud_mask(sat_image)
    sat_coastline = compute_coastline.compute_coastline(sat_image)
    sat_coastline_keypoints = correlate_images.get_keypoints(
        sat_coastline, scale_factor
    )

    # =====================ground image manupulations==================
    field_coords = read_config_files.field_coords(args.field_filename)
    ground_keypoints = read_ground_image.read_ground_keypoints(args.ground_kpts)

    # =====================aligning of the sat image==================
    align_result = correlate_images.compute_transform_from_keypoints(
        sat_coastline_keypoints, ground_keypoints
    )
    homography, align_was_successful = align_result
    if not align_was_successful:
        print("cannot continue further, bad align")
        downlink.send_message_down("ALIGN UNSUCCESSFUL")
        sys.exit("ALIGN UNSUCCESSFUL")

    base_h, base_w = ground_keypoints.shape
    sat_image = SatImage(
        image=cv2.warpPerspective(
            sat_image.data, homography, (base_h, base_w), flags=cv2.INTER_NEAREST
        )
    )

    # =========================beam results back(for the sat)====================
    poly_points = np.flip(field_coords, axis=1)
    polygon = crop_field.Polygon(poly_points)

    # code for the sat
    only_field = crop_field.select_only_field(sat_image, polygon)
    average_color = np.average(only_field.data, axis=(0, 1))
    downlink.send_message_down(str(average_color))
    sky_lens_index = (average_color[2] - average_color[1]) / (
        average_color[1] - average_color[0]
    )
    print(f"skylens: {sky_lens_index}")
    print(f"NDVI: {(2.48 - sky_lens_index)/4.26}")


if __name__ == "__main__":
    scale_factor = (10, 10)
    sat_main(scale_factor)
