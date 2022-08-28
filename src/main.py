import argparse
import os
import sys

import cv2
import numpy as np
import matplotlib.pyplot as plt

from preprocessing import cloud_mask
from processing import compute_coastline, correlate_images
from time_and_shoot import shoot
from time_and_shoot.sat_image import SatImage


def precompute_coastline():
    base_image = cv2.imread("./monkedir/base_image_example.tiff")
    final_image_data = compute_coastline.compute_coastline(SatImage(image=base_image))
    final_image_data = final_image_data.data.astype(np.uint8) * 255
    cv2.imwrite("./monkedir/precomputed_coastline.tiff", final_image_data)


def sat_main():
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

    computed_coastline = SatImage(
        image=cv2.cvtColor(
            cv2.imread(args.computed_coastline) * 255, cv2.COLOR_BGR2GRAY
        )
    )

    time_to_take_picture = "2022:09:03,12:00:00,000"
    # take picture
    sat_image = shoot.take_picture(time_to_take_picture)
    sat_image = cloud_mask.mask_clouds(sat_image)
    sat_coastline = compute_coastline.compute_coastline(sat_image)

    print(computed_coastline.data.shape)
    print(sat_coastline.data.shape)
    # plt.imshow(computed_coastline.data)
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
    base_image_rgb = cv2.imread("./monkedir/base_image_example.tiff")
    base_image_rgb = np.flip(base_image_rgb, axis=2)
    ax1.imshow(base_image_rgb)
    ax2.imshow(np.flip(back_transformed_sat_image, axis=2))
    plt.show()


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
    print(transformed_coords.shape)
    # for point, trans_point in zip(field_coords_px, transformed_coords):
    #     p = point[0]
    #     tp = trans_point[0]
    #     area = 100
    #     ax1.scatter(p[0], p[1], s=area, color="red")
    #     ax2.scatter(tp[0], tp[1], s=area, color="red")

    # ax1.axline((0, 0), (500, 500), color="black")
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
    # precompute_coastline()
    # sat_main()
    presentation_images()
