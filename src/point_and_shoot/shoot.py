from .sat_image import SatImage
import os
import numpy as np
import rasterio

def take_picture() -> SatImage:
    """
    A fucntion which interfaces with the camera of the satellite and returns a picture. This function should be called right after the point
    function. 
    Args: TBD 
    returns: An image and its metadata, TBD
    """ 
    image_filename = os.path.join("/", "home", "vasil", "mission-endurance", "data", "Clipped_Bulgaria.tif")
    modified_image_filename = os.path.join("/", "home", "vasil", "mission-endurance", "data", "Clipped_Bulgaria_modified.tif")

    # make the image uint8, with max value 255
    with rasterio.open(image_filename, "r+") as image:
        profile = image.profile
        profile.update(
            dtype=rasterio.uint8,
        )
        image_data = image.read((3, 2, 1))

        max_value = image_data.max()
        print(image_data.min(), image_data.max())
        image_data = image_data / (max_value/254.99)
        image_data = image_data.astype(np.uint8)
        print(image_data.min(), image_data.max())

    with rasterio.open(modified_image_filename, "w", **profile) as mod_image:
        mod_image.write(image_data)
        pass
     
    return SatImage(modified_image_filename, 1) 



