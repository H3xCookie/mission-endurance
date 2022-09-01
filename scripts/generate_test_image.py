import rasterio


def shift_given_image():
    filename = "./monkedir/stacked_rgb.tiff"
    offset_filename = "./monkedir/offset_stacked_rgb.tiff"
    with rasterio.open(filename) as base_image:
        data = base_image.read()
        height, width = data.shape[1:]
        meta = base_image.meta
        new_height, new_width = int(0.9 * height), int(0.92 * width)
        offset_height, offset_width = int(0.05 * height), int(0.02 * width)
        meta.update(height=new_height, width=new_width)
        with rasterio.open(offset_filename, "w", **meta) as sat_image:
            for i in range(3):
                sat_image.write_band(
                    i + 1,
                    data[
                        i,
                        offset_height : offset_height + new_height,
                        offset_width : offset_width + new_width,
                    ],
                )


if __name__ == "__main__":
    shift_given_image()
