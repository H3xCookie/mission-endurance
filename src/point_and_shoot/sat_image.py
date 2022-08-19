import rasterio

class SatImage:
    def __init__(self, image_filename):
        """
        pass the full path of the file which contains the image, preferably in .tif format
        """
        self.image = rasterio.open(image_filename) 

    def __del__(self):
        print("image was closed: ", self.image.closed)
        self.image.close()
        print("image was closed: ", self.image.closed)

