from .sat_image import SatImage
import numpy as np
import rasterio
import matplotlib.pyplot as plt


def take_picture_from_file(filename, bands) -> SatImage:
    """
    takes an image filaneme(.tif) and bands, a tuple of ints specifying which bands should the output have, ex. (4, 3, 2) if we want RGB
    returns SatImage with shape (len(bands), height, width)
    """
    image_name = "".join(filename.split(".")[:-1])
    band_info = "_".join([str(b) for b in bands])
    modified_image_filename = f"./{image_name}_{band_info}.tif"

    # make the image uint8, with max value 255
    with rasterio.open(filename, "r+") as image:
        new_profile = image.profile
        new_profile.update(dtype=rasterio.uint8, count=len(bands))
        image_data = image.read(bands)

        # use np.max() for absolutely correct solution
        max_value = np.quantile(image_data, 0.9999)

        image_data = image_data / (max_value / 254.99)
        image_data = np.clip(image_data, 0, 255)
        image_data = image_data.astype(np.uint8)

    # overwrites if a previous image exists
    with rasterio.open(modified_image_filename, "w", **new_profile) as mod_image:
        mod_image.write(image_data)
        pass

    return SatImage(bands, filename=modified_image_filename)


def take_picture() -> SatImage:
    """
    A fucntion which interfaces with the camera of the satellite and returns a picture. This function should be called right after the point
    function.
    Args: TBD
    returns: A `SatImage` class, which wraps around the tif produced by the satellite
    """
    # TODO
    return SatImage((0, 0, 0), filename="monke.tif")
