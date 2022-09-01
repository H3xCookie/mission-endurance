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

    setup_camera.turn_on_camera()
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
    # x then y coordinate

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
    # good_fields = [
    #     [[4135, 2130], [4239, 2140], [4321, 2059], [4224, 1931]],
    #     [[3623, 1791], [3739, 1764], [3710, 1552], [3566, 1562]],
    # ]
    # needs to be of shape (n, 1, 2) to be able to be acted on by homography
    # field_coords_px = np.array(points).reshape((len(points), 1, 2))
    # # flip because y coord should be before x coord
    # field_coords_px = np.flip(field_coords_px, axis=2)

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
    for index, points in enumerate(good_fields):
        # pass aligned image and coordinates to image recognition algorithm
        poly_points = np.flip(np.array(points).reshape((len(points), 2)), axis=1)
        print(poly_points)
        if input("continue?") != "y":
            break
        polygon = crop_field.Polygon(poly_points)
        print("make field mask")
        field_mask = crop_field.filter_polygon(sat_image.data.shape, polygon).reshape(
            (base_h, base_w, 1)
        )
        # print("get filtered sat image")
        # filtered_sat_image = SatImage(image=sat_image.data * field_mask)
        # print("only_field")
        # only_field = crop_field.crop_filtered_image(filtered_sat_image)
        print("crop image to field")
        only_field = crop_field.crop_image_to_field(sat_image.data, field_mask)

        # compute the Green index of the field
        print("compute index")
        green_index = indeces.green_index(only_field)

        downlink.send_message_down(
            f"{green_index}: {make_decision.is_field_planted(green_index)}"
        )
        ax[0][index].imshow(only_field.data)
    for index, points in enumerate(bad_fields):
        # pass aligned image and coordinates to image recognition algorithm
        poly_points = np.flip(np.array(points).reshape((len(points), 2)), axis=1)
        print(poly_points)
        if input("continue?") != "y":
            break
        polygon = crop_field.Polygon(poly_points)
        print("make field mask")
        field_mask = crop_field.filter_polygon(sat_image.data.shape, polygon).reshape(
            (base_h, base_w, 1)
        )
        # print("get filtered sat image")
        # filtered_sat_image = SatImage(image=sat_image.data * field_mask)
        # print("only_field")
        # only_field = crop_field.crop_filtered_image(filtered_sat_image)
        print("crop image to field")
        only_field = crop_field.crop_image_to_field(sat_image.data, field_mask)

        # compute the Green index of the field
        print("compute index")
        green_index = indeces.green_index(only_field)

        downlink.send_message_down(
            f"{green_index}: {make_decision.is_field_planted(green_index)}"
        )
        ax[1][index].imshow(only_field.data)
    # fig, ax = plt.subplots(1, 2)
    # ax[0].imshow(sat_image.data)
    # ax[1].imshow(only_field.data)
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
