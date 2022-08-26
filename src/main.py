import argparse
import os
import sys

import cv2
import matplotlib.pyplot as plt

from coastline import compute_coastline, correlate_images


def main():
    """
    Pass a coastline file, corresponding to the coastline computed on Earth, and an image from the satellite
    """
    parser = argparse.ArgumentParser(description="Prepare .tif image for ML model")
    # parser.add_argument("--coastline", required=True)
    parser.add_argument("--sat_image", required=True)
    parser.add_argument("--im", required=True)
    args = parser.parse_args()
    base_image = compute_coastline.compute_coastline(args.sat_image)
    transformed_image = compute_coastline.compute_coastline(args.im)
    print("computed base and transformed coastlines")

    trans_back_image = correlate_images.compute_affine_transform(
        base_image, transformed_image
    )

    print(trans_back_image)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(base_image)
    ax2.imshow(trans_back_image)
    plt.show()


if __name__ == "__main__":
    main()
