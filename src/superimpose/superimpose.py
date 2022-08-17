from point_and_shoot.shoot import SatImage 
import os
import shapefile as shp

def filter_image(original_image: SatImage, shapefile) -> SatImage:
    """
    takes a SatImage object and a shapefile corresponding to a field on that image, and makes it so that everything outisde the shapefile
    has a color (0, 0, 0). 
    returns: SatImage which has been filtered of the pixels outside of the field 
    """
    # TODO 
    shapefile_filename = os.path.join("/", "home", "vasil", "mission-endurance", "data", "bulgaria2.shp")
    sf = shp.Reader(shapefile_filename)
    print(sf)
    # shapes = sf.shapes()
    # my_poly = sf.shapes(0)
    return original_image

