# mission-endurance

## Table of contents

1. [Program description](#program-description)
2. [Software modules](#software-modules)
    1. [`point_and_shoot`](#point_and_shoot)
    2. [`superimpose`](#superimpose)
    3. [`image_analysis`](#image_analysis)

## Program description

When the satellite is given a command to shoot a field, it points to that particular field and takes a photo. For testing this will be emulated by the `point_and_shoot` module returning SENTINEL-2 images, together with their metadata. With the given `Field` object, we come up with some math to superimpose the field on the image, so that we know which pixels are inside the field and which are not. Afterwards we can feed those pixels/the whole image to a model which, together with time of the picture, would determine whether the field has anything planted on it. If it sees a field which has noting planted on it, send info back to Earth. 

## Software modules

### `point_and_shoot`

pass

### `superimpose`

pass

### `image_analysis`

pass



<!-- ## 1. Preliminary data gathering from OLAF -->

<!-- Get information of each field which is subsidized by the EU, preferably as a shapefile. Get metadata, such as supposed crop type, approximate time of planting etc. --> 

<!-- ## 2. Take pictures of the fields -->

<!-- Point the satellite to the given fields and take pictures before, during and after harvest time for each given field. For testing use SENTINEL data (same resolution). Output should be image with metadata for sat position, so we can later convert to a geocentric coordinate system. --> 

<!-- ## 3. Get training data for models -->
<!-- Pls Shelly make it work pls -->

<!-- ### Recognising if a field is planted with crops or already harvested -->

<!-- Need an index of (image, shapefile, crop status), train the model on individual pixels inside the shapefile (only color information). -->

<!-- ### Identifying the crop type of the unharvested fields -->

<!-- Same info as top section, but with crop type instead of crop/no_crop. --> 

<!-- ## 4. Image analysis -->

<!-- Run the images with shapefiles against ML models 1 and 2 to determine what crop is there on every field, or if it is harvested. If anything unusual is reported, contact ground with relevant images, as well as the analysis performed in space. --> 


