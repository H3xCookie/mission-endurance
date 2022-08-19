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

        # show the image and the shapefiles
        fig, ax = plt.subplots()
        bounds = [image.bounds[0], image.bounds[2], image.bounds[1], image.bounds[3]]
        
        ax = rasterio.plot.show(image, extent=bounds, ax=ax)
        data["geometry"].plot(ax=ax)
        plt.show()

    # create new file with name <image_filename>_modified.<image_extension>
    upper_path = os.path.abspath(os.path.dirname(original_image.image_filename))
    filename = os.path.basename(original_image.image_filename)
    name = "".join(filename.split(".")[:-1])
    extension = filename.split(".")[-1]
    new_name = name+"_modified"+extension

    # with rasterio.open(new_name, "w") as new_image:
    #     new_image.write()
    return original_image


