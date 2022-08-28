from time_and_shoot.sat_image import SatImage


def take_picture_from_file(filename) -> SatImage:
    """
    takes an image filaneme(.tif) and bands, a tuple of ints specifying which bands should the output have, ex. (4, 3, 2) if we want RGB
    returns SatImage with shape (len(bands), height, width)
    """
    return SatImage(filename=filename)


def take_picture(time_of_picture) -> SatImage:
    """
    A fucntion which interfaces with the camera of the satellite and returns a picture. !TBD it recieves the time at which to take the picture, waits until then, takes a picture and returns it.

    Args: TBD
    returns: A `SatImage` class, which wraps around the tif produced by the satellite
    """
    # TODO
    return take_picture_from_file("./monkedir/transformed_image.tiff")
