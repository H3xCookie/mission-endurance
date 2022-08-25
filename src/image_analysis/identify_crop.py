from superimpose.superimpose import MLModelInput
import numpy as np


def ndvi_of_field(filtered_image: MLModelInput) -> float:
    """
    identifies what is most likely to be on the image
    filtered_image: A MLModelInput which has had the pixels outside of the field of interest blackened out
    returns: float, corresponding to the average ndvi of the field
    """
    zero_nums = np.count_nonzero(filtered_image.data, axis=(1, 2))
    area = filtered_image.data.shape[1] * filtered_image.data.shape[2]
    average_color = (
        np.average(filtered_image.data, axis=(1, 2))
        * area
        / (area - np.average(zero_nums))
    )
    print(average_color)
    bands = list(filtered_image.bands)
    nir_indeces = [index for index, b in enumerate(bands) if b == 8]
    red_indeces = [index for index, b in enumerate(bands) if b == 4]
    print(nir_indeces, red_indeces)
    if len(nir_indeces) == 0 or len(red_indeces) == 0:
        print("error")
        raise Exception(
            "to compute ndvi we need the filtered_indeces_image to have band 8 and 4"
        )
    # indeces of nir_indeces and red_indeces bands in the MLModelInput.bands tuple
    nir_index = nir_indeces[0]
    red_index = red_indeces[0]
    print(nir_index, red_index)
    nir = average_color[nir_index]
    red = average_color[red_index]
    print(f"NIR: {nir}, Red: {red}")
    ndvi = (nir - red) / (nir + red)
    return ndvi
