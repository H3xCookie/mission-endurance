import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import rasterio

blue_fn = sys.argv[1]
green_fn = sys.argv[2]
red_fn = sys.argv[3]

meta = {}
with rasterio.open(blue_fn) as band:
    band_data = band.read(1)

    meta = band.meta

print(meta)
meta.update(count=3, driver="GTiff", dtype=np.uint8)
print(meta)

stacked_rgb_fn = sys.argv[4]
filenames = [blue_fn, green_fn, red_fn]
with rasterio.open(os.path.join(stacked_rgb_fn), "w", **meta) as stack:
    for index, filename in enumerate(filenames):
        with rasterio.open(filename) as band:
            band_data = band.read(1)

            print(band_data.dtype)
            print(np.max(band_data))
            band_data = np.clip(band_data.astype(np.float16) / 255, 0, 255).astype(
                np.uint8
            )
            stack.write_band(index + 1, band_data)
