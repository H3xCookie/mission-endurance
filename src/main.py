import sys
import os
import geopandas as gpd
from point_and_shoot import point, shoot
from superimpose import superimpose

def main():
    """
    pass the folder which contains the merged.tif file, without the _PROCESSED part, as an argument to main
    """
    folder = sys.argv[1].split(".")[0]
    image_location = os.path.join(os.getcwd(), "OUTPUT_TIF", f"{folder}_PROCESSED", "merged.tif")
    location = (0, 0)
    point.point(location)
    image = shoot.take_picture_from_file(image_location)

    shapefile_filename = os.path.join("/", "home", "vasil", "mission-endurance", "data", "farm_shapefiles.zip")
    data = gpd.read_file(shapefile_filename)
    print(data["geometry"].centroid)
    filtered_image = superimpose.filter_image(image, data)
    print(filtered_image.data.shape)

if __name__ == "__main__":
    main()
