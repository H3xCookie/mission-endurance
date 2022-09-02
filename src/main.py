import argparse

import cv2
import matplotlib.pyplot as plt
import numpy as np

from communications import downlink
from image_analysis import indeces, make_decision
from preprocessing import cloud_mask, precompute_coastline
from processing import compute_coastline, correlate_images, crop_field
from time_and_shoot import setup_camera, shoot
from time_and_shoot.sat_image import SatImage


def sat_main():
    """
    the main fn which runs on the satellite. fiedl coords must
    be in the form (x, y), and be in counter-clockwise direction in the coordinate system of the image(x right, y down).
    """
    parser = argparse.ArgumentParser(description="Pass precomputed coastline")
    parser.add_argument("--computed_coastline", required=True)
    args = parser.parse_args()

    # TODO Setup camera for real satellite
    # setup_camera.turn_on_camera()
    # take picture
    time_to_take_picture = "2022:09:03,12:00:00,000"
    print("take picture")
    sat_image = shoot.take_picture(time_to_take_picture)
    height, width = sat_image.data.shape[:2]

    # plt.imshow(np.flip(sat_image.data, axis=2))
    # plt.show()
    print("sat image h, w: ", height, width)
    # add mask attribute to the image
    print("compute cloud mask of picture")
    # sat_image.mask = cloud_mask.cloud_mask(sat_image)
    print("compute coastline of picture")
    sat_coastline = compute_coastline.compute_coastline(sat_image)

    # x then y coordinate, need to flip them later so y is first, then x
    good_fields = [
        [[4335, 2563], [4452, 2691], [4553, 2608], [4444, 2475]],
        [[3364, 2228], [3394, 2322], [3420, 2231]],
        [[4631, 2274], [4658, 2188], [4625, 2185], [4586, 2239]],
    ]

    bad_fields = [
        [[2958, 3493], [2964, 3525], [3072, 3471], [3078, 3419]],
        [[3884, 3464], [3902, 3351], [3800, 3328]],
        [[4212, 3482], [4215, 3545], [4312, 3488]],
    ]

    print("load precomputed coastline")
    computed_coastline = precompute_coastline.load_precomputed_coastline(
        args.computed_coastline
    )

    # compute and apply homography to the original sat image
    print("compute homography")
    homography = correlate_images.compute_affine_transform(
        computed_coastline, sat_coastline
    )
    # h, w = sat_image.data.shape[:2]
    print("warp sat image to ground image")
    base_h, base_w = computed_coastline.data.shape[:2]
    print("precomputed coastline h, w: ", base_h, base_w)
    # plt.imshow(sat_image.data)
    # plt.show()
    sat_image = SatImage(
        image=cv2.warpPerspective(
            sat_image.data, homography, (base_h, base_w), flags=cv2.INTER_NEAREST
        )
    )
    fig, ax = plt.subplots(2, 3)
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
            downlink.send_message_down(f"{green_index}: {is_planted}")
            ax[dataset_index][index].imshow(only_field.data)
            ax[dataset_index][index].title.set_text(
                f"green coeff {green_index: .2f}: {is_planted}"
            )
    plt.show()


if __name__ == "__main__":
    sat_main()
