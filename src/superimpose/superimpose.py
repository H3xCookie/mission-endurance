from point_and_shoot.shoot import SatImage 

def filter_image(original_image: SatImage, shapefile) -> SatImage:
    """
    takes a SatImage object and a shapefile corresponding to a field on that image, and makes it so that everything outisde the shapefile
    has a color (0, 0, 0). 
    returns: SatImage which has been filtered of the pixels outside of the field 
    """
    # TODO 
    return original_image
