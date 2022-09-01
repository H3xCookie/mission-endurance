import os

import matplotlib.pyplot as plt
import numpy as np
from time_and_shoot.sat_image import SatImage


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

    def polygon_range(self):
        """
        returns (xmin, xmax, ymin, ymax)
        """
        return (
            np.min(self.points[:, 1]),
            np.max(self.points[:, 1]),
            np.min(self.points[:, 0]),
            np.max(self.points[:, 0]),
        )


def select_only_field(sat_image: SatImage, polygon: Polygon) -> MLModelInput:
    minx, maxx, miny, maxy = polygon.polygon_range()
    points = polygon.points
    n = int(points.shape[0])
    coords = np.array(
        np.meshgrid(
            np.arange(start=miny, stop=maxy),
            np.arange(start=minx, stop=maxx),
            indexing="ij",
        ),
        dtype=np.uint16,
    )
    coords = np.moveaxis(coords, 0, 2)
    final_arr = np.ones(coords.shape[:2], dtype=bool)

    for i in range(n):
        i1 = (i + 1) % n
        r = points[i1] - points[i]
        # rotation counter-clockwise by 90 degrees
        normal_vec = np.zeros((2,))
        normal_vec[0], normal_vec[1] = -r[1], r[0]
        final_arr &= np.dot(coords - points[i], normal_vec) > 0

    return sat_image.data[miny:maxy, minx:maxx, :] * final_arr[:, :, np.newaxis]


def filter_polygon(begin_array_shape, polygon: Polygon) -> np.ndarray:
    minx, maxx, miny, maxy = polygon.polygon_range()
    points = polygon.points
    n = int(points.shape[0])
    coords = np.array(
        np.meshgrid(
            np.arange(start=miny, stop=maxy),
            np.arange(start=minx, stop=maxx),
            indexing="ij",
        ),
        dtype=np.uint16,
    )
    # coords = np.array(
    #     np.meshgrid(
    #         np.arange(begin_array_shape[0]),
    #         np.arange(begin_array_shape[1]),
    #         indexing="ij",
    #     ),
    #     dtype=np.uint16,
    # )
    coords = np.moveaxis(coords, 0, 2)
    final_arr = np.ones(coords.shape[:2], dtype=bool)

    for i in range(n):
        i1 = (i + 1) % n
        r = points[i1] - points[i]
        # rotation counter-clockwise by 90 degrees
        normal_vec = np.zeros((2,))
        normal_vec[0], normal_vec[1] = -r[1], r[0]
        final_arr &= np.dot(coords - points[i], normal_vec) > 0

    return final_arr


# def crop_filtered_image(filtered_image: SatImage) -> MLModelInput:
#     data = filtered_image.data
#     nonzero_y, nonzero_x = np.nonzero(data)[:2]
#     min_x, max_x = (
#         np.min(nonzero_x),
#         np.max(nonzero_x),
#     )
#     min_y, max_y = (
#         np.min(nonzero_y),
#         np.max(nonzero_y),
#     )

#     cropped_data = data[min_y:max_y, min_x:max_x, :]

#     return MLModelInput(data=cropped_data)


# def crop_image_to_field(
#     sat_image_data: np.ndarray, field_mask: np.ndarray
# ) -> MLModelInput:
#     nonzero_y, nonzero_x = np.nonzero(field_mask)[:2]
#     min_x, max_x = (
#         np.min(nonzero_x),
#         np.max(nonzero_x),
#     )
#     min_y, max_y = (
#         np.min(nonzero_y),
#         np.max(nonzero_y),
#     )
#     print("sat image shape: ", sat_image_data.shape)
#     return MLModelInput(data=(sat_image_data * field_mask)[min_y:max_y, min_x:max_x, :])
