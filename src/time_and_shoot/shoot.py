import datetime
import os
import subprocess
import time
from datetime import datetime, timezone

import numpy as np

from time_and_shoot.sat_image import SatImage


def take_picture_from_file(filename) -> SatImage:
    """
    takes an image filaneme(.tif) and bands, a tuple of ints specifying which bands should the output have, ex. (4, 3, 2) if we want RGB
    returns SatImage with shape (len(bands), height, width)
    """
    return SatImage(filename=filename)


def take_picture(unix_timestamp) -> SatImage:
    """
    A fucntion which interfaces with the camera of the satellite and returns a picture. It returns the image in BGR format, so SatImage.data[0] is the blue band
    returns: A `SatImage` class, which wraps around the tif produced by the satellite
    """
    print(f"should take a picture in {unix_timestamp}")
    filename = "./monkedir/rotated_namibia_picture.tiff"
    print(f"the satellite image is {filename}")
    # flip picture since it is already in bgr
    picture = take_picture_from_file(filename)
    return SatImage(image=np.flip(picture.data, axis=2))
