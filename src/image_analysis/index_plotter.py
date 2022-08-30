import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt


def index(red, green, blue):
return (red - green) / (red + green)


def sample_band(band: np.ndarray, N=500):
    flat_band = band.flatten()
    area = len(flat_band)
    indeces = np.arange(start=0, stop=area, step=int(area / N))
    return np.take(flat_band, indeces)


def plot_index():
    image_filename = os.path.join(".", "data", "OUTPUT_TIF", "merged.tif")
    image = rasterio.open(image_filename)
    # B, G, R, NIR
    data = image.read((1, 2, 3, 7))
    should_take_pixel = np.all(data > 10, axis=0)

    blue, green, red, nir = data.astype(np.float32)

    blue = blue[should_take_pixel]
    green = green[should_take_pixel]
    red = red[should_take_pixel]
    nir = nir[should_take_pixel]

    sampled_blue = sample_band(blue)
    sampled_green = sample_band(green)
    sampled_red = sample_band(red)
    sampled_nir = sample_band(nir)

    ndvi = 1 - 2 * sampled_red / (sampled_red + sampled_nir)

    print("NDVI min max")
    print(np.min(ndvi), np.max(ndvi))
    our_index = index(sampled_red, sampled_green, sampled_blue)
    print("NDVI min max")
    print(np.min(our_index), np.max(our_index))

    plt.scatter(ndvi, our_index, s=1)
    plt.show()


if __name__ == "__main__":
    # a1 = np.array([1, 2, 3, 4])
    # a2 = np.array([4, 5, 6, 7])
    # print((a2 - a1) / (a2 + a1))
    # print(1 - 2 * a1 / (a2 + a1))
    plot_index()
