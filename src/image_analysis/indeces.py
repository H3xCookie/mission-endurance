import numpy as np
from processing.crop_field import MLModelInput


def green_index(filtered_image: MLModelInput) -> float:
    average_color = np.average(filtered_image.data, axis=(0, 1))
    print(average_color)
    b, g, r = average_color

    return (r - g) / (g - b)
