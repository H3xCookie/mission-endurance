import os

import numpy as np


def field_coords(field_coords_filename):
    """
    recieves a pass folder, maybe the name of the folder which contains that pass data, and return and ndarray of shape (n_points, 2), where n_points is the number of points of the border of the field, first x then y coordinate.
    returns: np.ndarray
    """
    with open(field_coords_filename, "r") as file:
        lines = file.readlines()
    coords_array = []
    for line in lines:
        x, y = line.split(",")[:2]
        coords_array.append([int(x), int(y)])
    coords_array = np.array(coords_array)
    return coords_array


def time_of_photo(time_filename):
    """
    returns the utc timestamp in seconds
    """
    with open(time_filename, "r") as time_file:
        line = time_file.readline()

    return float(line)
