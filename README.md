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

First we pick a field next to a coastline, for easier correlation of coordinate systems. We compute the coastline for the same area from an image on Earth. We take note of the corners of this field in the coordinate system of the Earth photo. Let this system be $E$. In $E$ we compute the coordinates of the coastline, and send some identifiable features, such as corners, and send them to space. Once the satellite takes a photo, it detects clouds and computes the coastline on its photo, using the same algorithm. Then we determine the affine transformation which takes $P$ to $E$, which maps the Platform-1 coastline to the coastline we precomputed on Earth. Then we transform the Platform-1 image using this transformation. This has the effect of aligning the satellite image with the one on Earth. Then we can use the field coordinates in $E$, and compute an index based on the average color of the field. Since this index is correlated with how much vegetation there is on the field, based on its value we can determine whether the field has crops planted on it. Then the satellite beams that information back to earth.

## Software modules

### `config_scripts/`

Contains the config files which tell the satellite which field it should image, at what time the program should take a picture and which coastline file should it use. 

### `scripts`

#### Satellite scripts

The `run.sh` and `zip_all_sat_files.sh` scripts are meant to run on the satellite. First we need to compress all files for the satellite using `zip_all_sat_files.sh`, which creates a `.tar.gz` file. We transfer it and the `run.sh` script on the satellite. The only command that needs to be run on the satellite is `./run.sh`. It unzips the source code files and runs the main function.

#### Utility scripts

Contains scripts useful for downloading sentinel data and turning it into useful data for the program. Since we are running the scripst on the ground only, they use a dedicated conda environment `geo-env/`. The `scripts/rgb_from_safe.py` script takes as an input the location of a `.SAFE` folder, as unzipped from the Sentinel website, and produces an RGB .tiff image immediately inside the `.SAFE` folder. Then the `src/preprocessing/precompute_coastline.py` can take the RGB image as input to compute its coastline, and save it as identifiable keypoints, such as corners.

### `main.py` 

Takes as an `--ground_keypoints` input the pickled points (`.pkl`), which have been precomputed on the ground. It runs insie the `sat-env\` virtual environment, which is an exact copy of the one on Platform-1. Its logic is as follows: 
1. Receive the coordinates of the field in pixels on the image on the ground
2. Identify the clouds and throw away the image if target field is covered
3. Compute the transformation between the Platform-1 and the Sentinel images
4. Crop only the field from the satellite photo.
5. Compute a "greenness" index, based on which we decide whether the field is planted or not.
6. Send the result back to Earth

### `read_config`

Reads the `config_files` directory containing information for each pass in separate folders. `read_config/read_config_files.py` has functions dealing with configuration files such as coordinates of the field and the exact time at which we need to take a picture.

### `time_and_shoot`

Recieves the time at which is should shoot the image, waits unitl the time comes and takes a picture. It also provides the `SatImage` class, which wraps all other images in the code. 

### `preprocessing`

Removes cloud cover and loads the precomputed coastline keypoints. The keypoints are a pickled `Keypoints` class, implemented in `src/processing/correlate_images.py`. 

### `processing`

Computes the coastline on the satellite as an identifiable feature, correlates it with features of the precomputed coastline which is already on the sat and determines the homography between the Platform-1 photo and the one on the ground. It performs this homography on the Platform-1 image to get an aligned image, whose features coincide with the ones on the picture on the ground. It crops a polygon corresponding to the field of interest out of the satellite picture, in order to easily pass it around to the decision making module.

### `communications`

An interface to the downlinking of the satellite. Creates downlink file in `/work/transfer` directory of the payload computer. When the satellite perfrom the data downlink mission, OBC will automatically transfer file from `/work/transfer` directory to ground station.

## Library Environment

Library environment of pyaload computer in PLATFORM-1 can be found in "lib.txt" on [our github](https://github.com/vasilNnikolov/mission-endurance/blob/plat-1-running/libs.txt)

## PLATFORM-1 Specification

1. SSO ~530 km
2. 31 MP camera (6464 H x 4852 V)
3. 30 m resolution picture
4. 3-axis stabilizing, Nadir pointing when taking a photo (point toward center of the Earth)
5. Pointing accuracy up to 0.2 degree
6. 50 kB uplink and downlink data per satellite pass

