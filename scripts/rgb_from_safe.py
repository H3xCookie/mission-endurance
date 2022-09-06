import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import rasterio

safe_filename = sys.argv[1]

granule = os.path.join(safe_filename, "GRANULE")
weird_folder = os.listdir(granule)[0]
all_images_folder = os.path.join(granule, weird_folder, "IMG_DATA")
images = sorted(os.listdir(all_images_folder))

print(sorted(images))

indeces = [4, 3, 2, 8]
# extract metadata for one image
meta = {}
im_filename = os.path.join(all_images_folder, images[indeces[0] - 1])
with rasterio.open(im_filename) as band:
    band_data = band.read(1)
    print(band.shape)
    meta = band.meta

meta.update(count=4, driver="GTiff", dtype=np.uint8)
print(meta)

with rasterio.open(
    os.path.join(safe_filename, "rgbnir_image_2.tif"), "w", **meta
) as stack:
    for num_index, index in enumerate(indeces):
        im_filename = os.path.join(all_images_folder, images[index - 1])
        print(f"num_index: {num_index}, filename: {im_filename}")
        with rasterio.open(im_filename) as band:
            band_data = band.read(1)
            print(band_data.dtype)
            print(np.max(band_data))
            band_data = np.clip(band_data.astype(np.float16) / 255, 0, 255).astype(
                np.uint8
            )
            stack.write_band(num_index + 1, band_data)

# with rasterio.open(os.path.join(safe_filename, "stacked_rgb.tif")) as stack:
#     plt.imshow(np.moveaxis(stack.read(), 0, 2))
#     plt.show()
