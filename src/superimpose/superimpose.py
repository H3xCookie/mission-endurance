from point_and_shoot.shoot import SatImage 
import geopandas as gpd
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt
import os

def filter_image(original_image: SatImage, shapefile) -> SatImage:
    """
    takes a SatImage object and a shapefile corresponding to a field on that image, and makes it so that everything outisde the shapefile
    has a color (0, 0, 0). 
    returns: SatImage which has been filtered of the pixels outside of the field 
    """
    # TODO 
    shapefile_filename = os.path.join("/", "home", "vasil", "mission-endurance", "data", "farm_shapefiles.zip")
    data = gpd.read_file(shapefile_filename)
    image_filename = os.path.join("/", "home", "vasil", "mission-endurance", "data", "Clipped_Bulgaria.tif")
    image = rio.open(image_filename)
    # works only for EPSG coordinate system
    image_crs_index = int(str(image.crs).split(":")[1])
    data = data.to_crs(image_crs_index)
    print(data.crs, image.crs)

    # show the image and the shapefiles
    fig, ax = plt.subplots()
    bounds = [image.bounds[0], image.bounds[2], image.bounds[1], image.bounds[3]]
    ax = rio.plot.show(image, extent=bounds, ax=ax, cmap='pink')
    data.plot(ax=ax)
    plt.show()
    return original_image

