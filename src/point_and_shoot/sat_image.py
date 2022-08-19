
class SatImage:
    def __init__(self, image_filename, metadata):
        """
        pass the full path of the file which contains the image, preferably in .tif format
        """
        self.image_filename = image_filename
        self.metadata = metadata

