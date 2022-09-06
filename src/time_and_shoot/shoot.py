import datetime
import os
import subprocess
from datetime import timezone
from time import sleep

import numpy as np

from time_and_shoot.sat_image import SatImage


def take_picture_from_file(filename) -> SatImage:
    """
    takes an image filaneme(.tif) and bands, a tuple of ints specifying which bands should the output have, ex. (4, 3, 2) if we want RGB
    returns SatImage with shape (len(bands), height, width)
    """
    return SatImage(filename=filename)


def utc_timestamp():
    return (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )


def take_picture(utc_time_for_picture) -> SatImage:
    """
    A fucntion which interfaces with the camera of the satellite and returns a picture. It returns the image in BGR format, so SatImage.data[0] is the blue band

    returns: A `SatImage` class, which wraps around the tif produced by the satellite
    """
    # TODO test
    # # approx time it takes for the sat to take a photo
    # time_delay = 4
    # while utc_timestamp() < utc_time_for_picture - time_delay:
    #     sleep(0.5)

    # subprocess.run(["./src/take_picture.sh"])
    # picture_filename = os.listdir(
    #     "/work/mission-endurance/monkedir/sat_captured_images/"
    # )[0]
    # return take_picture_from_file(picture_filename)
    filename = "./config_files/pass_1/sat_image_3_bgr.tiff"
    print(f"the satellite image is {filename}")
    # flip picture since it is already in bgr
    picture = take_picture_from_file(filename)
    return SatImage(image=np.flip(picture.data, axis=2))
