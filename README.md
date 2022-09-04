
# mission-endurance
Some text

## Table of contents

1. [Program description](#program-description)
2. [Software modules](#software-modules)
    1. [`time_and_shoot`](#time_and_shoot)
    2. [`preprocessing`](#preprocessing)
    3. [`processing`](#processing)
    4. [`image_analysis`](#image_analysis)
    5. [`communications`](#communications)

## Program description

First we pick a field next to a coastline, for easier correlation of coordinate systems. We compute the coastline for the same area from an image on Earth. We take note of the corners of this field in the coordinate system of the Earth photo. Let this system be $E$. In $E$ we compute the coordinates of the coastline, maybe list of pixels, TBD. We send it to space. Once the satellite takes a photo, it removes clouds and computes the coastline using the same algorithm. Then we determine the affine transformation from $E$ to $P$, which maps the earth coastline to the Platform-1 coastline. Using it we compute the 4 corners of the field in $P$ and then take some index of the pixels inside. 

## Example usage

## Software modules

### `scripts`

#### Running scripts

The `zip_all_sat_files.sh` script zips all the files in `src/` and the pickled `.pkl` file containing the precomputed keypoints, and creates a single archive which is to be used on the satellite. The `run.sh` script is the only command that needs to be run on the satellite, which unzips that same archive, and calls the `main.py` file.

#### Utility scripts

Contains scripts useful for downloading sentinel data and turning it into a tiff. Since we are running the scripts on the ground only, they use a dedicated conda environment `geo-env/`. The `rgb_from_safe.py` script takes as an input the location of a `.SAFE` folder, as unzipped from the Sentinel website, and produces a .tiff image immediately inside the `.SAFE` folder. 

### `main.py` 

Recieves the `--computed_coastline` .tiff image as input and runs the main function of the satellite. It runs inside the `sat-env` virtual environment, as defined by `libs.txt`. It's logic is as follows: 
1. Receive the coordinates of the field in pixels on the image on the ground
2. Filter the clouds and throw away the image if target field is covered 
3. Computes the transformation between the Platform-1 and the Sentinel images
4. Crop only the field from the satellite photo.
5. Compute a "greenness" index, based on which we decide whether the field is planted or not.

### `time_and_shoot`

Recieves the time at which is should shoot the image, waits unitl the time comes and takes a picture. It also provides the `SatImage` class, which wraps all other images in the code. 

### `preprocessing`

Removes cloud cover and loads the coastline image. At the moment it only saves the coastline as a boolean .tiff, TODO improve.

### `processing`

Computes the coastline as an identifiable feature, correlates it with features of the precomputed coastline which is already on the sat and determines the homography between the sat photo and the one on the ground. It performs this homography on the Platform-1 image to get an aligned image, whose features coincide with the ones on the picture on the ground. Crops a polygon corresponding to the field out of the satellite picture, in order to easily pass it around to the decision making module.

### `image_analysis`

Analyses the filtered image (where all the points outside the field are blackened). It tries to determine whether something is planted on the field. Provides a "greenness" index based on the bands of the image, equal to $I = \frac{RED - GREEN}{GREEN - BLUE}$. The higher the index, the higher the chance a field is planted.

### `communications`

An interface to the downlinking of the satellite. TODO implement!!!
