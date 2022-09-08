import datetime
import json
import os
import re
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


def take_picture(job_path, unix_timestamp) -> SatImage:
    """
    A fucntion which interfaces with the camera of the satellite and returns a picture. It returns the image in BGR format, so SatImage.data[0] is the blue band
    returns: A `SatImage` class, which wraps around the tif produced by the satellite
    """
    time_delay = 4
    # the unix time in seconds
    print(f"approx start of the program is {datetime.utcnow().timestamp()}")
    while datetime.utcnow().timestamp() < unix_timestamp - time_delay:
        time.sleep(0.1)

    interface_with_camera(job_path)
    rgb_image = take_picture_from_file("./image_custom.tiff")

    # flip it because the satellite gives images in RGB and all the code works with BGR
    return SatImage(image=np.flip(rgb_image.data, axis=2))


def interface_with_camera(job_path):
    camera_client = "/usr/bin/es_rpiMgrClient"
    camera_exec = subprocess.Popen(
        [camera_client, "camera", "--capture", job_path, "-t", "tiff", "-p", "1"],
        stdout=subprocess.PIPE,
    )
    camera_response_str = camera_exec.communicate()[0].decode("utf-8")
    p = re.compile("{'status': .*")
    camera_response_jsons = p.findall(camera_response_str)
    if len(camera_response_jsons) == 0:
        print("Camera Error: " + camera_response_str)
        return

    q = re.compile("'")
    camera_json_str = q.sub('"', camera_response_jsons[0])
    camera_json = json.loads(camera_json_str)
    print(camera_json)
    image_file = camera_json["value"]
    try:
        if os.path.isfile(image_file):
            os.rename(image_file, job_path + "image_custom.tiff")
    except:
        pass
