from superimpose.superimpose import MLModelInput

def ndvi_of_field(filtered_image: MLModelInput) -> float:
    """
    identifies what is most likely to be on the image
    filtered_image: A MLModelInput which has had the pixels outside of the field of interest blackened out
    returns: float, corresponding to the average ndvi of the field 
    """
    # TODO


