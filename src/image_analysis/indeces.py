import numpy as np
from processing.crop_field import MLModelInput


def green_index(filtered_image: MLModelInput) -> float:
    height, width = filtered_image.data.shape[:2]
    non_zero_nums = np.count_nonzero(filtered_image.data, axis=(0, 1))
    area = height * width
    coeff = area / np.average(non_zero_nums)

    average_color = np.average(filtered_image.data, axis=(0, 1)) * coeff
    print(average_color)
    b, g, r = average_color

    return (r - g) / (g - b)
