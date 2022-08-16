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

Provides the `point` and `shoot` functions, as well as representations for the image (maybe a class), which is easier to pass around the code.

### `superimpose`

pass

### `image_analysis`

pass

