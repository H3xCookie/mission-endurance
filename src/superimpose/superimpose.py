from time_and_shoot.sat_image import SatImage
import numpy as np
import matplotlib.pyplot as plt
import os


class MLModelInput:
    def __init__(self, bands, data: np.ndarray):
        """
        bands: a tuple of the band numbers in sentinel notation. len(bands) = n_channels. Ex. bands = (4, 3, 2) means R, R, B
        data: np.ndarray of shape (n_channels, height, width). If n_channels=3 they are R, G, B
        """
        self.bands = bands
        self.data: np.ndarray = data


def get_RGB(image: MLModelInput) -> np.ndarray:
    bands = list(image.bands)
    red_indeces = [index for index, b in enumerate(bands) if b == 4]
    green_indeces = [index for index, b in enumerate(bands) if b == 3]
    blue_indeces = [index for index, b in enumerate(bands) if b == 2]
    if len(red_indeces) == 0 or len(green_indeces) == 0 or len(blue_indeces) == 0:
        print("error")
        raise Exception("we need band 4, 3 and 2 to compute RGB")
    # indeces of nir_indeces and red_indeces bands in the MLModelInput.bands tuple
    im_data = image.data
    return np.stack(
        [im_data[red_indeces[0]], im_data[green_indeces[0]], im_data[blue_indeces[0]]],
        axis=2,
    )


def filter_image(
    band_filtered_image: SatImage, shapefile: gpd.GeoDataFrame
) -> MLModelInput:
    """
    takes a SatImage object and a shapefile corresponding to a field on that image, and makes it so that everything outisde the shapefile
    has a color (0, 0, 0).
    band_filtered_image: An SatImage wrapper of an already created .tif image, with correct metadata and filtered by useful bands
    shapefile: shapefile read by `gpd.read_file(<path_to_shapefile>.zip)`
    returns: SatImage which has been filtered of the pixels outside of the field
    """
    # works only for EPSG coordinate system
    band_filtered_image_crs_index = int(
        str(band_filtered_image.image.crs).split(":")[1]
    )
    # make shapefile to be in the same coordinate system as image
    data = gpd.GeoDataFrame(shapefile.to_crs(band_filtered_image_crs_index))

    cropped_image = rioxarray.open_rasterio(band_filtered_image.image).rio.clip(
        data["geometry"][[1]], data.crs
    )

    output = MLModelInput(band_filtered_image.bands, cropped_image.data)
    plt.imshow(get_RGB(output))
    plt.title("RGB representation of the fields")
    plt.show()

    return output
