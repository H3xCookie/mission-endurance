from point_and_shoot.shoot import SatImage 
import numpy as np
import geopandas as gpd
import rasterio, rasterio.plot
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
    with rasterio.open(original_image.image_filename) as image:
        # works only for EPSG coordinate system
        image_crs_index = int(str(image.crs).split(":")[1])
        data = gpd.GeoDataFrame(shapefile.to_crs(image_crs_index))
        polygons = list(data["geometry"])
        interesting_polygon = polygons[0]

        
        # show the image and the shapefiles
        fig, ax = plt.subplots()
        bounds = [image.bounds[0], image.bounds[2], image.bounds[1], image.bounds[3]]
        
        ax = rasterio.plot.show(image, extent=bounds, ax=ax)
        our_series = gpd.GeoSeries([interesting_polygon])
        # data["geometry"].plot(ax=ax)
        our_series.plot(ax=ax)
        plt.show()
        return original_image


