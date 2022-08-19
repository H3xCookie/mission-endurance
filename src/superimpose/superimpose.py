from point_and_shoot.shoot import SatImage 
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon, Point
import rasterio, rasterio.plot
import rioxarray
import matplotlib.pyplot as plt
import os


def filter_image(original_image: SatImage, shapefile: gpd.GeoDataFrame) -> SatImage:
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
     
    cropped_image = rio_image.rio.clip(data["geometry"], data.crs)

    fig, (ax1, ax2) = plt.subplots(1, 2)

    rio_image.plot.imshow(ax=ax1)
    data["geometry"].plot(ax=ax1)
    cropped_image.plot.imshow(ax=ax2)
    plt.show()
    

    return original_image


