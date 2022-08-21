from point_and_shoot.shoot import SatImage 
import numpy as np
import geopandas as gpd
import rasterio, rasterio.plot
import rioxarray
import matplotlib.pyplot as plt
import os

class MLModelInput:
    def __init__(self, data):
        """
        data: np.ndarray of shape (n_channels, height, width). If n_channels=3 they are R, G, B
        """
        self.data = data

def filter_image(original_image: SatImage, shapefile: gpd.GeoDataFrame) -> MLModelInput:
    """
    takes a SatImage object and a shapefile corresponding to a field on that image, and makes it so that everything outisde the shapefile
    has a color (0, 0, 0). 
    original_image: An SatImage wrapper of an already created .tif image, with correct metadata and in RGB format (ch. 1 is R, ch. 2 is G,
    ch. 3 is B)
    shapefile: shapefile read by `gpd.read_file(<path_to_shapefile>.zip)`
    returns: SatImage which has been filtered of the pixels outside of the field 
    """
    image = original_image.image # rasterio image
    # works only for EPSG coordinate system
    original_image_crs_index = int(str(image.crs).split(":")[1])
    # make shapefile to be in the same coordinate system as image
    data = gpd.GeoDataFrame(shapefile.to_crs(original_image_crs_index))

    rio_image = rioxarray.open_rasterio(image)
     
    cropped_image = rio_image.rio.clip(data["geometry"][[0]], data.crs)

    fig, ax = plt.subplots()
    # rio_image.plot.imshow(ax=ax)

    # data["geometry"].plot(ax=ax)
    cropped_image.plot.imshow(ax=ax)
    plt.show()
    return MLModelInput(cropped_image.data)

