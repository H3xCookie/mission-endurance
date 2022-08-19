import os
import geopandas as gpd
from point_and_shoot import point, shoot
from superimpose import superimpose

def main():
    location = (0, 0)
    point.point(location)
    image = shoot.take_picture()

    shapefile_filename = os.path.join("/", "home", "vasil", "mission-endurance", "data", "farm_shapefiles.zip")
    data = gpd.read_file(shapefile_filename)
    filtered_image = superimpose.filter_image(image, data)
    print(filtered_image.data.shape)


if __name__ == "__main__":
    main()
