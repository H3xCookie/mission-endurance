from point_and_shoot.shoot import SatImage 
import numpy as np
import geopandas as gpd
import rasterio, rasterio.plot
import matplotlib.pyplot as plt
import os

def filter_image(original_image: SatImage, shapefile) -> SatImage:
    """
    takes a SatImage object and a shapefile corresponding to a field on that image, and makes it so that everything outisde the shapefile
    has a color (0, 0, 0). 
    returns: SatImage which has been filtered of the pixels outside of the field 
    """
    shapefile_filename = os.path.join("/", "home", "vasil", "mission-endurance", "data", "farm_shapefiles.zip")
    data = gpd.read_file(shapefile_filename)

    print(data["geometry"][0])
    image_filename = os.path.join("/", "home", "vasil", "mission-endurance", "data", "Clipped_Bulgaria.tif")
    modified_image_filename = os.path.join("/", "home", "vasil", "mission-endurance", "data", "Clipped_Bulgaria_modified.tif")

    # make the image uint8, with max value 255
    with rasterio.open(image_filename, "r+") as image:
        profile = image.profile
        profile.update(
            dtype=rasterio.uint8,
        )
        image_data = image.read((3, 2, 1))

        max_value = image_data.max()
        print(image_data.min(), image_data.max())
        image_data = image_data / (max_value/254)
        image_data = image_data.astype(np.uint8)
        print(image_data.min(), image_data.max())

    with rasterio.open(modified_image_filename, "w", **profile) as mod_image:
        mod_image.write(image_data)
        pass

    with rasterio.open(modified_image_filename) as image:
        # works only for EPSG coordinate system
        image_crs_index = int(str(image.crs).split(":")[1])
        data = data.to_crs(image_crs_index)
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


