import matplotlib.pyplot as plt
import numpy as np
import rasterio


def index(red, green, blue):
    # return (red - green) / (green - blue)
    return green / (red + blue)


def sample_band(band: np.ndarray, N=5000):
    flat_band = band.flatten()
    area = len(flat_band)
    print(area)
    indeces = np.arange(start=0, stop=area, step=int(area / N))
    return np.take(flat_band, indeces)


def plot_index():
    with rasterio.open("monkedir/bgrnir_image_1.tiff") as image:
        # B, G, R, NIR
        data = image.read((1, 2, 3, 4))

        blue, green, red, nir = data.astype(np.float32)
        print(data.shape)
        should_take_pixel = np.all(data > 10, axis=0)
        print(np.min(data, axis=(1, 2)), np.max(data, axis=(1, 2)))

        blue = blue[should_take_pixel]
        green = green[should_take_pixel]
        red = red[should_take_pixel]
        nir = nir[should_take_pixel]

        sampled_blue = sample_band(blue)
        sampled_green = sample_band(green)
        sampled_red = sample_band(red)
        sampled_nir = sample_band(nir)

        ndvi = (sampled_nir - sampled_red) / (sampled_red + sampled_nir)

        print("NDVI min max")
        print(np.min(ndvi), np.max(ndvi))
        our_index = index(sampled_red, sampled_green, sampled_blue)
        print("our index min max")
        print(np.min(our_index), np.max(our_index))

        plt.scatter(ndvi, our_index, s=1)
        # plt.ylim((-5, 5))
        plt.show()


if __name__ == "__main__":
    plot_index()
