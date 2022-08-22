from .sat_image import SatImage
import os
import numpy as np
import rasterio
def take_picture_from_file(filename) -> SatImage:
    """
    opens a .tif GeoTIFF image 
    returns: An image and its metadata, TBD
    """ 
    modified_image_filename = os.path.join("/", "home", "vasil", "mission-endurance", "data", "Clipped_Bulgaria_modified.tif")

    # make the image uint8, with max value 255
    with rasterio.open(filename, "r+") as image:
        new_profile = image.profile
        new_profile.update(
            dtype=rasterio.uint8,
            count=3
        )
        image_data = image.read((2, 3, 4))

        max_value = image_data.max()
        image_data = image_data / (max_value/254.99)
        image_data = image_data.astype(np.uint8)
        print(image_data.shape)

    with rasterio.open(modified_image_filename, "w", **new_profile) as mod_image:
        mod_image.write(image_data)
        pass
     
    return SatImage(filename=modified_image_filename) 

def take_picture() -> SatImage:
    """
    A fucntion which interfaces with the camera of the satellite and returns a picture. This function should be called right after the point
    function. 
    Args: TBD 
    returns: An image and its metadata, TBD
    """ 
    image_filename = os.path.join(
        "/", 
        "home", "vasil", "mission-endurance", "Output",
        "S2B_MSIL2A_20220731T085559_N0400_R007_T35TNH_20220731T103425_PROCESSED", 
        "merged.tif"
    )
    modified_image_filename = os.path.join("/", "home", "vasil", "mission-endurance", "data", "Clipped_Bulgaria_modified.tif")

    # make the image uint8, with max value 255
    with rasterio.open(image_filename, "r+") as image:
        new_profile = image.profile
        new_profile.update(
            dtype=rasterio.uint8,
            count=3
        )
        image_data = image.read((2, 3, 4))

        max_value = image_data.max()
        image_data = image_data / (max_value/254.99)
        image_data = image_data.astype(np.uint8)
        print(image_data.shape)

    with rasterio.open(modified_image_filename, "w", **new_profile) as mod_image:
        mod_image.write(image_data)
        pass
     
    return SatImage(filename=modified_image_filename) 



