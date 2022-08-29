
# mission-endurance

## Table of contents

1. [Program description](#program-description)
2. [Software modules](#software-modules)
    1. [`time_and_shoot`](#time_and_shoot)
    2. [`superimpose`](#superimpose)
    3. [`image_analysis`](#image_analysis)

## Program description

First we pick a field next to a coastline, for easier correlation of coordinate systems. We compute the coastline for the same area from an image on Earth. We take note of the corners of this field in the coordinate system of the Earth photo. Let this system be $E$. In $E$ we compute the coordinates of the coastline, maybe list of pixels, TBD. We send it to space. Once the satellite takes a photo, it removes clouds and computes the coastline using the same algorithm. Then we determine the affine transformation from $E$ to $P$, which maps the earth coastline to the Platform-1 coastline. Using it we compute the 4 corners of the field in $P$ and then take some index of the pixels inside. 

## Example usage

## Software modules

### `main.py` 

Pass a .tif image as an argument and shapefiles and it crops the image so only the shapefiles are visible, everything else is black. This is the input to any ML model we may use.

### `time_and_shoot`

Recieves the time at which is should shoot the image, takes a picture and saves it. It also provides the `SatImage` class, which wraps all other images in the code. 

### `preprocessing`

Removes cloud cover(TODO implement!) and computes/loads the coastline image. At the moment it only saves it as a boolean .tiff, TODO improve.

### `processing`

Computes the coastline as an identifiable feature, correlates it with features of the precomputed coastline which is already on the sat and determines the homography between the sat photo and the one on the ground. It performs this homography to get an aligned image, whose features coincide with the ones on the picture on the ground. Crops a polygon corresponding to the field out of the satellite picture, in order to easily pass it around.

### `image_analysis`

Analyses the filtered image (where all the points outside the field are blackened). It tries to determine whether something is on the field. Provides different indeces in which higher is more greenery.

### `communications`

An interface to the downlinking of the satellite. TODO implement!!!
