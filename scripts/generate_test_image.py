import cv2
import matplotlib.pyplot as plt
import numpy as np
import rasterio


def get_bgrnir_image():
    filename = "./data/OUTPUT_TIF/S2A_MSIL1C_20220527T085601_N0400_R007_T35TNH_20220527T110350_PROCESSED/merged.tif"
    ndvi_image = "./monkedir/bgrnir_image_1.tiff"
    with rasterio.open(filename) as base_image:
        data = base_image.read((2, 3, 4, 8))
        height, width = data.shape[1:]
        meta = base_image.meta
        meta.update(count=4)
        with rasterio.open(ndvi_image, "w", **meta) as sat_image:
            for i in range(4):
                sat_image.write_band(i + 1, data[i, :, :])


def scale_down_ground_image():
    # full_image = "./data/OUTPUT_TIF/S2A_MSIL1C_20220527T085601_N0400_R007_T35TNH_20220527T110350_PROCESSED/merged.tif"
    ground_image = "./stacked_bgr_namibia.tiff"
    offset_filename = "./monkedir/ground_image_namibia_color_boosted.tiff"
    with rasterio.open(ground_image) as sent_image:
        bgr_data = sent_image.read()
        print(bgr_data.dtype)
        bgr_data = bgr_data.astype(np.float16) * 2**8 / np.max(bgr_data)
        bgr_data = np.clip(bgr_data, 0, 255).astype(np.uint8)
        print(bgr_data.shape)
        height, width = bgr_data.shape[1:]
        meta = sent_image.meta
        new_height, new_width = int(height), int(width)
        offset_height, offset_width = int(0.00 * height), int(0.00 * width)
        meta.update(dtype=np.uint8, height=new_height, width=new_width)
        with rasterio.open(offset_filename, "w", **meta) as sat_image:
            for i in range(3):
                sat_image.write_band(
                    i + 1,
                    bgr_data[
                        i,
                        offset_height : offset_height + new_height,
                        offset_width : offset_width + new_width,
                    ],
                )


if __name__ == "__main__":
    # shift_given_image()
    scale_down_ground_image()
