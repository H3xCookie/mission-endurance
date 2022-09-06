import matplotlib.pyplot as plt
import numpy as np
import rasterio


def index(red, green, blue):
    return (red - green) / (green + blue)
    # return green / (red + blue)


def vari(red, green, blue):
    return (green - red) / (green + red - blue)


def sample_band(band: np.ndarray, N=50000):
    flat_band = band.flatten()
    area = len(flat_band)
    print(area)
    indeces = np.arange(start=0, stop=area, step=int(area / N))
    return np.take(flat_band.astype(np.float16), indeces)


def sample_patches(band: np.ndarray, N=5000):
    # return band
    height, width = band.shape
    area = height * width
    indeces = np.arange(start=0, stop=area, step=int(area / N))
    indeces = np.array([(int(t / width), t % width) for t in indeces])
    return np.array([np.average(band[x : x + 10, y : y + 10]) for (y, x) in indeces])


def plot_index():
    with rasterio.open("monkedir/rgbnir_image_2.tif") as image:
        # R,G,B NIR
        data = image.read()
        print(data.shape)
        height, width = data.shape[1:]
        data = data[:, : int(height / 4), : int(width / 4)]

        red, green, blue, nir = data.astype(np.float16)
        print(np.average(data, axis=(1, 2)))
        print(red.dtype)
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.imshow((nir - red) / (nir + red), cmap="gray")
        ax2.imshow(np.clip(vari(red, green, blue), -15, 15), cmap="gray")
        plt.show()
        # plt.imshow(2 * np.stack([red, green, blue], axis=2))
        # plt.show()
        print(data.shape)
        # should_take_pixel = np.all(data > 10, axis=0)
        # print(np.min(data, axis=(1, 2)), np.max(data, axis=(1, 2)))

        # blue = blue[should_take_pixel]
        # green = green[should_take_pixel]
        # red = red[should_take_pixel]
        # nir = nir[should_take_pixel]

        sampled_blue = sample_band(blue)
        sampled_green = sample_band(green)
        sampled_red = sample_band(red)
        sampled_nir = sample_band(nir)

        ndvi = (sampled_nir - sampled_red) / (sampled_red + sampled_nir)

        print("NDVI min max")
        print(np.min(ndvi), np.max(ndvi))
        our_index = vari(sampled_red, sampled_green, sampled_blue)
        print("our index min max")
        print(np.min(our_index), np.max(our_index))

        plt.scatter(ndvi, our_index, s=1)
        plt.show()


if __name__ == "__main__":
    plot_index()
