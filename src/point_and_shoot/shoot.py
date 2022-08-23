from .sat_image import SatImage
import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt
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
        bands = (4, 3, 2)
        image_data = image.read(bands)

        # use np.max() for absolutely correct solution
        max_value = np.quantile(image_data, 0.9999)

        image_data = image_data / (max_value/254.99)
        print(f"new image max: {image_data.max()}")
        image_data = np.clip(image_data, 0, 255)
        image_data = image_data.astype(np.uint8)
        fig, ax = plt.subplots(1, 3)
        for band in range(3):
            ax[band].hist(image_data[band, :, :].flatten(), bins=50)
        plt.show()
        
    with rasterio.open(modified_image_filename, "w", **new_profile) as mod_image:
        mod_image.write(image_data)
        pass
     
    return SatImage(filename=modified_image_filename) 

def take_bands(filename, bands):
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
        new_profile.update(
            dtype=rasterio.uint8,
            count=len(bands)
        )
        image_data = image.read(bands)

        # use np.max() for absolutely correct solution
        max_value = np.quantile(image_data, 0.9999)

        image_data = image_data / (max_value/254.99)
        image_data = np.clip(image_data, 0, 255)
        image_data = image_data.astype(np.uint8)

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



