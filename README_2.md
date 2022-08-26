
# mission-endurance

## Table of contents

1. [Program description](#program-description)
2. [Software modules](#software-modules)
    1. [`point_and_shoot`](#point_and_shoot)
    2. [`superimpose`](#superimpose)
    3. [`image_analysis`](#image_analysis)

## Program description

First we pick a field next to a coastline, for easier correlation of coordinate systems. We compute the coastline for the same area from an image on Earth. We take note of the corners of this field in the coordinate system of the Earth photo. Let this system be $E$. In $E$ we compute the coordinates of the coastline, maybe list of pixels, TBD. We send it to space. Once the satellite takes a photo, it removes clouds and computes the coastline using the same algorithm. Then we determine the affine transformation from $E$ to $P$, which maps the earth coastline to the Platform-1 coastline. Using it we compute the 4 corners of the field in $P$ and then take some index of the pixels inside. 

## Example usage

## Software modules

### `main.py` 

Pass a .tif image as an argument and shapefiles and it crops the image so only the shapefiles are visible, everything else is black. This is the input to any ML model we may use.

### `point_and_shoot`

Provides the `point` and `shoot` functions and the `SatImage` class, which stores the satellite image and its metadata.

### `superimpose`

Provides the `filter_image` function. It takes a sat image and the shapefile of a field on that image, and blackens out all pixels that are not inside the shapefile. NOTE!!! currently it only works with EPSG coordinate systems.

### `image_analysis`

Analyses the filtered image (where all the points outside the field are blackened). It tries to determine what is on the field.
