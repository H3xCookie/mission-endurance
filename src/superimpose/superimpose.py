from point_and_shoot.shoot import SatImage 
import numpy as np
import geopandas as gpd
import rasterio, rasterio.plot
import rioxarray
import matplotlib.pyplot as plt
import os

class MLModelInput:
    def __init__(self, bands, data):
        """
        bands: a tuple of the band numbers in sentinel notation. len(bands) = n_channels. Ex. bands = (4, 3, 2) means R, R, B
        data: np.ndarray of shape (n_channels, height, width). If n_channels=3 they are R, G, B
        """
        self.bands = bands
        self.data = data

def filter_image(band_filtered_image: SatImage, shapefile: gpd.GeoDataFrame) -> MLModelInput:
    """
    takes a SatImage object and a shapefile corresponding to a field on that image, and makes it so that everything outisde the shapefile
    has a color (0, 0, 0). 
    band_filtered_image: An SatImage wrapper of an already created .tif image, with correct metadata and filtered by useful bands 
    shapefile: shapefile read by `gpd.read_file(<path_to_shapefile>.zip)`
    returns: SatImage which has been filtered of the pixels outside of the field 
    """
    # works only for EPSG coordinate system
    band_filtered_image_crs_index = int(str(band_filtered_image.image.crs).split(":")[1])
    # make shapefile to be in the same coordinate system as image
    data = gpd.GeoDataFrame(shapefile.to_crs(band_filtered_image_crs_index))

    cropped_image = rioxarray.open_rasterio(band_filtered_image.image).rio.clip(data["geometry"][[1]], data.crs)
     
    fig, ax = plt.subplots()
    # rio_image.plot.imshow(ax=ax)

    # data["geometry"].plot(ax=ax)
    cropped_image.plot.imshow(ax=ax)
    plt.show()
    return MLModelInput(band_filtered_image.bands, cropped_image.data)

