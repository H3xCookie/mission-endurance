from time_and_shoot.sat_image import SatImage
import numpy as np
import matplotlib.pyplot as plt
import os


class MLModelInput:
    def __init__(self, data: np.ndarray):
        """
        data: np.ndarray of shape (height, width, 3). bands 0, 1 and 2 correspond to blue, green, red
        """
        self.data: np.ndarray = data


class Polygon:
    def __init__(self, points: np.ndarray):
        """
        points is an np.array of shape (n, 2). Points should be in a clockwise direction
        """
        self.points: np.ndarray = points


def filter_polygon(begin_array: np.ndarray, polygon: Polygon) -> np.ndarray:
    points = polygon.points
    n = int(points.shape[0])
    coords = np.array(
        np.meshgrid(
            np.arange(begin_array.shape[0]),
            np.arange(begin_array.shape[1]),
            indexing="ij",
        )
    )
    coords = np.moveaxis(coords, 0, 2)
    final_arr = np.ones_like(coords[:, :, 0], dtype=bool)

    for i in range(n):
        i1 = (i + 1) % n
        r = points[i1] - points[i]
        # rotation counter-clockwise by 90 degrees
        normal_vec = np.zeros((2,))
        normal_vec[0], normal_vec[1] = -r[1], r[0]
        final_arr = final_arr & (np.dot(coords - points[i], normal_vec) > 0)

    return final_arr


def crop_filtered_image(filtered_image: SatImage) -> MLModelInput:
    data = filtered_image.data
    nonzero_y, nonzero_x = np.nonzero(data)[:2]
    min_x, max_x = (
        np.min(nonzero_x),
        np.max(nonzero_x),
    )
    min_y, max_y = (
        np.min(nonzero_y),
        np.max(nonzero_y),
    )

    cropped_data = data[min_y:max_y, min_x:max_x, :]

    return MLModelInput(data=cropped_data)


# def get_RGB(image: MLModelInput) -> np.ndarray:
#     bands = list(image.bands)
#     red_indeces = [index for index, b in enumerate(bands) if b == 4]
#     green_indeces = [index for index, b in enumerate(bands) if b == 3]
#     blue_indeces = [index for index, b in enumerate(bands) if b == 2]
#     if len(red_indeces) == 0 or len(green_indeces) == 0 or len(blue_indeces) == 0:
#         print("error")
#         raise Exception("we need band 4, 3 and 2 to compute RGB")
#     # indeces of nir_indeces and red_indeces bands in the MLModelInput.bands tuple
#     im_data = image.data
#     return np.stack(
#         [im_data[red_indeces[0]], im_data[green_indeces[0]], im_data[blue_indeces[0]]],
#         axis=2,
#     )


# def filter_image(
#     band_filtered_image: SatImage, shapefile: gpd.GeoDataFrame
# ) -> MLModelInput:
#     """
#     takes a SatImage object and a shapefile corresponding to a field on that image, and makes it so that everything outisde the shapefile
#     has a color (0, 0, 0).
#     band_filtered_image: An SatImage wrapper of an already created .tif image, with correct metadata and filtered by useful bands
#     shapefile: shapefile read by `gpd.read_file(<path_to_shapefile>.zip)`
#     returns: SatImage which has been filtered of the pixels outside of the field
#     """
#     # works only for EPSG coordinate system
#     band_filtered_image_crs_index = int(
#         str(band_filtered_image.image.crs).split(":")[1]
#     )
#     # make shapefile to be in the same coordinate system as image
#     data = gpd.GeoDataFrame(shapefile.to_crs(band_filtered_image_crs_index))

#     cropped_image = rioxarray.open_rasterio(band_filtered_image.image).rio.clip(
#         data["geometry"][[1]], data.crs
#     )

#     output = MLModelInput(band_filtered_image.bands, cropped_image.data)
#     plt.imshow(get_RGB(output))
#     plt.title("RGB representation of the fields")
#     plt.show()

#     return output
