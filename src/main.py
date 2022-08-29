import argparse
import os
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np

from preprocessing import cloud_mask, precompute_coastline
from processing import compute_coastline, correlate_images, crop_field
from time_and_shoot import shoot
from time_and_shoot.sat_image import SatImage
from image_analysis import indeces, make_decision
from communications import downlink


def sat_main():
    """
    the main fn which runs on the satellite. fiedl coords must
    be in the form (x, y), and be in counter-clockwise direction in the coordinate system of the image(x right, y down).
    """
    # take picture
    time_to_take_picture = "2022:09:03,12:00:00,000"
    sat_image = shoot.take_picture(time_to_take_picture)
    sat_image = cloud_mask.mask_clouds(sat_image)
    sat_coastline = compute_coastline.compute_coastline(sat_image)

    points = [[462, 210], [469, 276], [525, 266], [516, 217]]
    # needs to be of shape (n, 1, 2) to be able to be acted on by homography
    field_coords_px = np.array(points).reshape((len(points), 1, 2))
    # flip because y coord should be before x coord
    field_coords_px = np.flip(field_coords_px, axis=2)

    parser = argparse.ArgumentParser(description="Pass precomputed coastline")
    parser.add_argument("--computed_coastline", required=True)
    args = parser.parse_args()

    computed_coastline = precompute_coastline.load_precomputed_coastline(
        args.computed_coastline
    )

    # compute and apply homography to the original sat image
    homography = correlate_images.compute_affine_transform(
        computed_coastline, sat_coastline
    )
    # h, w = sat_image.data.shape[:2]
    base_h, base_w = computed_coastline.data.shape[:2]
    aligned_image = SatImage(
        image=cv2.warpPerspective(
            sat_image.data, homography, (base_w, base_h), flags=cv2.INTER_NEAREST
        )
    )

    # pass aligned image and coordinates to image recognition algorithm
    polygon = crop_field.Polygon(field_coords_px.reshape((len(points), 2)))
    field_mask = crop_field.filter_polygon(aligned_image.data, polygon)
    filtered_image = SatImage(image=aligned_image.data * field_mask[:, :, np.newaxis])
    only_field = crop_field.crop_filtered_image(filtered_image)

    # compute the Green index of the field
    green_index = indeces.green_index(only_field)

    downlink.send_message_down(
        f"{green_index}: {make_decision.is_field_planted(green_index)}"
    )
    # fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    # base_image = cv2.imread("./monkedir/base_image_example.tiff")
    # ax1.imshow(base_image)
    # ax2.imshow(aligned_image.data)
    # ax3.imshow(only_field.data)
    # plt.show()


def presentation_images():
    """
    the main fn which runs on the satellite.
    """
    # needs to be of shape (n, 1, 2) to be able to be acted on by homography
    field_coords_px = np.array(
        [[496, 236], [527, 236], [527, 272], [496, 272]]
    ).reshape((4, 1, 2))
    parser = argparse.ArgumentParser(description="Pass precomputed coastline")
    parser.add_argument("--computed_coastline", required=True)
    args = parser.parse_args()
    # plot original and shifted sat image
    base_image = cv2.imread("./monkedir/base_image_example.tiff")
    trans_image = cv2.imread("./monkedir/transformed_image.tiff")
    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # ax1.imshow(np.flip(base_image, axis=2))
    # ax2.imshow(np.flip(trans_image, axis=2))
    # plt.show()

    computed_coastline = SatImage(
        image=cv2.cvtColor(
            cv2.imread(args.computed_coastline) * 255, cv2.COLOR_BGR2GRAY
        )
    )

    time_to_take_picture = "2022:09:03,12:00:00,000"
    sat_image = shoot.take_picture(time_to_take_picture)
    sat_image = cloud_mask.mask_clouds(sat_image)
    sat_coastline = compute_coastline.compute_coastline(sat_image)
    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # ax1.imshow(computed_coastline.data)
    # ax2.imshow(sat_coastline.data)
    # plt.show()

    homography = correlate_images.compute_affine_transform(
        computed_coastline, sat_coastline
    )
    # apply homography to the original sat image
    h, w = sat_image.data.shape[:2]
    back_transformed_sat_image = cv2.warpPerspective(
        sat_image.data, homography, (w, h), flags=cv2.INTER_NEAREST
    )

    fig, (ax1, ax2) = plt.subplots(1, 2)
    base_image_bgr = cv2.imread("./monkedir/base_image_example.tiff")
    ax1.imshow(np.flip(base_image_bgr, axis=2))
    ax2.imshow(np.flip(sat_image.data, axis=2))

    # compute the coordinates of the other field
    transformed_coords = cv2.perspectiveTransform(
        field_coords_px.astype(np.float32), np.linalg.inv(homography)
    )
    n = len(field_coords_px)
    for i in range(n):
        ax1.plot(
            [field_coords_px[i, 0, 0], field_coords_px[(i + 1) % n, 0, 0]],
            [field_coords_px[i, 0, 1], field_coords_px[(i + 1) % n, 0, 1]],
            color="red",
        )
        ax2.plot(
            [transformed_coords[i, 0, 0], transformed_coords[(i + 1) % n, 0, 0]],
            [transformed_coords[i, 0, 1], transformed_coords[(i + 1) % n, 0, 1]],
            color="red",
        )

    plt.show()


if __name__ == "__main__":
    # precompute_coastline.precompute_coastline()
    sat_main()
    # presentation_images()
