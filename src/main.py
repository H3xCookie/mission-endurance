import argparse
import os
import sys

import cv2
import numpy as np
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

    homography = correlate_images.compute_affine_transform(
        base_image, transformed_image
    )
    h, w = transformed_image.shape
    # !IMPORTANT images have to be uint8 for warpPerspective
    transformed_image = transformed_image.astype(np.uint8) * 255
    fin = cv2.warpPerspective(
        transformed_image, homography, (w, h), flags=cv2.INTER_NEAREST
    )
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(base_image)
    ax2.imshow(fin)
    plt.show()


if __name__ == "__main__":
    main()
