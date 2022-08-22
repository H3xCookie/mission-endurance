# mission-endurance

## Table of contents

1. [Program description](#program-description)
2. [Software modules](#software-modules)
    1. [`point_and_shoot`](#point_and_shoot)
    2. [`superimpose`](#superimpose)
    3. [`image_analysis`](#image_analysis)

## Program description

When the satellite is given a command to shoot a field, it points to that particular field and takes a photo. For testing this will be emulated by the `point_and_shoot` module returning SENTINEL-2 images, together with their metadata. With the given `Field` object, we come up with some math to superimpose the field on the image, so that we know which pixels are inside the field and which are not. Afterwards we can feed those pixels/the whole image to a model which, together with time of the picture, would determine whether the field has anything planted on it. If it sees a field which has noting planted on it, send info back to Earth. 

## Example usage

First we identify an area of interest and pick shapefiles of some fields in that area. We run `./scripts/sent_to_tif.sh` with the correct location data, cloud coverage and dates of interest. By default it downloads one image in the given window, can be modified. This creates a GeoTIFF file in `./data/OUTPUT_TIF/<image_name>_PROCESSED/merged.tif`. Pass that as an `--image` argument to `./src/main.py`, it will create `MLModelInput` class, which is the final data used for analysis.

## Software modules

### `sent_to_tif.sh`

Calls the API and converts the images to .tif GeoTIFF images. Stores them in a separate folder (`./data/PRODUCT_ZIP`).

### `main.py` 

Pass a .tif image as an argument and shapefiles and it crops the image so only the shapefiles are visible, everything else is black. This is the input to any ML model we may use.

### `point_and_shoot`

Provides the `point` and `shoot` functions and the `SatImage` class, which stores the satellite image and its metadata.

### `superimpose`

Provides the `filter_image` function. It takes a sat image and the shapefile of a field on that image, and blackens out all pixels that are not inside the shapefile. NOTE!!! currently it only works with EPSG coordinate systems.

### `image_analysis`

Analyses the filtered image (where all the points outside the field are blackened). It tries to determine what is on the field.
