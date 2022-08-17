from point_and_shoot.shoot import SatImage 
import geopandas as gpd
import rasterio as rio
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
    image_crs_index = int(str(image.crs).split(":")[1])
    data = data.to_crs(image_crs_index)
    print(data.crs, image.crs)
    return original_image

