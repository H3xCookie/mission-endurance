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


def sent_image_to_two_rgbs():
    full_image = "./data/OUTPUT_TIF/S2A_MSIL1C_20220527T085601_N0400_R007_T35TNH_20220527T110350_PROCESSED/merged.tif"
    ground_image = "./monkedir/ground_image_1_rgb.tiff"
    offset_filename = "./monkedir/sat_image_1_rgb.tiff"
    with rasterio.open(full_image) as sent_image:
        bgr_data = sent_image.read((2, 3, 4))
        print(bgr_data.dtype)
        bgr_data = bgr_data * 2**16 / np.max(bgr_data)
        bgr_data = bgr_data.astype(np.float32) / 255
        bgr_data = np.clip(bgr_data, 0, 255).astype(np.uint8)
        print(bgr_data.shape)
        height, width = bgr_data.shape[1:]
        meta = sent_image.meta
        meta.update(count=3, dtype=np.uint8)
        with rasterio.open(ground_image, "w", **meta) as ground:
            ground.write_band(1, bgr_data[0, :, :])
            ground.write_band(2, bgr_data[1, :, :])
            ground.write_band(3, bgr_data[2, :, :])
            new_height, new_width = int(0.9 * height), int(0.92 * width)
            offset_height, offset_width = int(0.05 * height), int(0.02 * width)
            meta.update(height=new_height, width=new_width)
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
    shift_given_image()
    # sent_image_to_two_rgbs()
