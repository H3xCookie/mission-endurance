import datetime
import os
import subprocess
import time
from datetime import datetime

import numpy as np

from sat_image import SatImage


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
    # TODO test; approx time it takes for the sat to take a photo
    # time_delay = 4
    # # the unix time in seconds
    # print(datetime.utcnow().timestamp())
    # while datetime.utcnow().timestamp() < unix_timestamp - time_delay:
    #     time.sleep(0.5)

    # subprocess.run(["./src/take_picture.sh"])
    # picture_filename = os.listdir(
    #     "/work/mission-endurance/monkedir/sat_captured_images/"
    # )[0]
    # rgb_image = take_picture_from_file(picture_filename)

    # # flip it because the satellite gives images in RGB and all the code works with BGR
    # return SatImage(image=np.flip(rgb_image.data, axis=2))

    print(f"should take a picture in {unix_timestamp}")
    filename = "./remove_this_dir/rotated_namibia_picture.tiff"
    print(f"the satellite image is {filename}")
    # flip picture since it is already in bgr
    picture = take_picture_from_file(filename)
    return SatImage(image=np.flip(picture.data, axis=2))
