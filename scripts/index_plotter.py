import matplotlib.pyplot as plt
import numpy as np
import rasterio


def index(red, green, blue):
    return (red - green) / (green + blue)


def vari(red, green, blue):
    return (green - red) / (green + red - blue)


def sample_band(band: np.ndarray, N=50000):
    flat_band = band.flatten()
    area = len(flat_band)
    print(area)
    indeces = np.arange(start=0, stop=area, step=int(area / N))
    return np.take(flat_band.astype(np.float16), indeces)


def sample_patches(band: np.ndarray, N=50000):
    # return band
    height, width = band.shape
    area = height * width
    indeces = np.arange(start=0, stop=area, step=int(area / N))
    indeces = np.array([(int(t / width), t % width) for t in indeces])
    return np.array([np.average(band[x : x + 10, y : y + 10]) for (y, x) in indeces])


def plot_index():
    with rasterio.open("monkedir/rgbnir_image_correct_scaling.tif") as image:
        # R,G,B NIR
        data = image.read()
        print(data.shape)
        height, width = data.shape[1:]
        data = data[:, : int(height / 4), : int(width / 4)]

        red, green, blue, nir = data.astype(np.float16)
        print(np.average(data, axis=(1, 2)))
        # fig, (ax1, ax2) = plt.subplots(1, 2)
        # ax1.imshow((nir - red) / (nir + red), cmap="gray")
        # ax2.imshow(np.clip(index(red, green, blue), -15, 15), cmap="gray")
        # plt.show()

        # plot shelly index vs ndvi
        sampled_blue = sample_band(blue)
        sampled_green = sample_band(green)
        sampled_red = sample_band(red)
        sampled_nir = sample_band(nir)

        ndvi = (sampled_nir - sampled_red) / (sampled_red + sampled_nir)

        print("NDVI min max")
        print(np.min(ndvi), np.max(ndvi))
        our_index = index(sampled_red, sampled_green, sampled_blue)

        def polyfit(x, y, degree):
            results = {}

            coeffs = np.polyfit(x, y, degree)

            # Polynomial Coefficients
            results["polynomial"] = coeffs.tolist()

            # r-squared
            p = np.poly1d(coeffs)
            # fit values, and mean
            yhat = p(x)  # or [p(z) for z in x]
            ybar = np.sum(y) / len(y)  # or sum(y)/len(y)
            ssreg = np.sum(
                (yhat - ybar) ** 2
            )  # or sum([ (yihat - ybar)**2 for yihat in yhat])
            sstot = np.sum((y - ybar) ** 2)  # or sum([ (yi - ybar)**2 for yi in y])
            results["determination"] = ssreg / sstot

            return results

        res = polyfit(ndvi.astype(np.float64), our_index.astype(np.float64), 1)
        line_coefficients = res["polynomial"]
        r_squared = res["determination"]

        print(line_coefficients)
        print(r_squared)
        print("our index min max")
        print(np.min(our_index), np.max(our_index))

        plt.scatter(ndvi, our_index, s=0.1)
        plt.plot(ndvi, np.poly1d(line_coefficients)(ndvi), color="r")
        plt.show()


if __name__ == "__main__":
    plot_index()
