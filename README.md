# MISSION-ENDURANCE
The ENDURANCE Cubesat mission is a joint project between three parties namely IBM, RedHat and ENDUROSAT who aim to democratizing access to space and make space accessible to everyone on this planet. With passion to inspire the next generation of future space explorers and leaders, the ENDURANCE mission gives students worldwide an opportunity to control a real spacecraft by sending their own developed code to control a 6U Cubesat in space. With 31 MP payload camera, Linux based Quad-core computer and many sensors installed within the satellite, students can have hand-on experience on how to develop and perform Edge Computing in space.

We, Sky-Lens (Endurance Team 1), want to use this opportunuty to demonstrate on how this ENDURANCE mission works and create an example project/guideline on how to deveop codes to run in space. Our main mission of this program is to take a picture at one specific area that has been pre-selected from ground mission control and run image processing codes to geolocate agricultural land in the taken picture and analyze whether the land has been cultivated or not. 

## Table of contents

- [MISSION-ENDURANCE](#mission-endurance)
  - [Table of contents](#table-of-contents)
  - [Program description](#program-description)
  - [Example usage](#example-usage)
  - [Software modules](#software-modules)
    - [`scripts`](#scripts)
    - [`main.py`](#mainpy)
    - [`time_and_shoot`](#time_and_shoot)
    - [`preprocessing`](#preprocessing)
    - [`processing`](#processing)
    - [`image_analysis`](#image_analysis)
    - [`communications`](#communications)
  - [Library Environment](#library-environment)
  - [PLATFORM-1 Specification](#platform-1-specification)

## Program description

First we pick a field next to a coastline, for easier correlation of coordinate systems. We compute the coastline for the same area from an image on Earth. We take note of the corners of this field in the coordinate system of the Earth photo. Let this system be $E$. In $E$ we compute the coordinates of the coastline, maybe list of pixels, TBD. We send it to space. Once the satellite takes a photo, it removes clouds and computes the coastline using the same algorithm. Then we determine the affine transformation from $E$ to $P$, which maps the earth coastline to the Platform-1 coastline. Using it we compute the 4 corners of the field in $P$ and then take some index of the pixels inside. 

## Example usage

## Software modules

### `scripts`

Contains scripts useful for downloading sentinel data and turning it into a tiff. `scripts/rgb_from_tiff.py` takes in as an argument the location of the `.SAFE` folder and creates a stacked rgb image inside it. Since we are running the scripst on the ground only, they use a dedicated conda environment `geo-env/`. The `rgb_from_safe.py` script takes as an input the location of a `.SAFE` folder, as unzipped from the Sentinel website, and produces a .tiff image immediately inside the `.SAFE` folder. Then the `src/preprocessing/precompute_coastline.py` can take it as an input to compute its coastline, and save it in whichever representation is more efficient (keypoints, image, etc.).

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

An interface to the downlinking of the satellite. Create downlink file in /work/transfer directory of the payload computer. When the satellite perfrom the data downlink mission, OBC will automatically transfer file from /work/transfer directory to ground station.

## Library Environment

Library environment of pyaload computer in PLATFORM-1 can be found in "lib.txt" on [our github](https://github.com/vasilNnikolov/mission-endurance/blob/plat-1-running/libs.txt)

## PLATFORM-1 Specification

1. SSO ~530 km
2. 31 MP camera (6464 H x 4852 V)
3. 30 m resolution picture
4. 3-axis stabilizing, Nadir pointing when taking a photo (point toward center of the Earth)
5. Pointing accuracy up to 0.2 degree
6. 50 kB uplink and downlink data per satellite pass

