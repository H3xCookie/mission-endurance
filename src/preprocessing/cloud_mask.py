import cv2
import matplotlib.pyplot as plt
import numpy as np
from time_and_shoot.sat_image import SatImage


def cloud_mask(image: SatImage) -> np.ndarray:
    """
    mask the clouds. returns a np.ndarray from bools, true is usable data, false is cloud
    """
    # load the image and perform pyramid mean shift filtering to aid the thresholding step
    w, h, bands = image.data.shape
    shifted = cv2.pyrMeanShiftFiltering(image.data, 21, 51)

    # convert the mean shift image to grayscale, then apply
    # Otsu's thresholding
    gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    thresh = cv2.bitwise_not(thresh)
    print(type(thresh))
    # TODO prly can return tresh
    res = cv2.bitwise_and(image.data, image.data, mask=thresh)
    res = res > 0
    res = res.astype(bool)
    print("computed cloud mask")
    return res

