import rasterio

class SatImage:
    def __init__(self, **kwargs):
        """
        pass either image=rasterio.DatasetReader or filename=<fullpath>.tif
        """
        if "image" not in kwargs and "filename" not in kwargs:
            print("specify either image=rasterio.DatasetReader or filename=<fullpath>.tif")
        if "filename" in kwargs:
            self.image = rasterio.open(kwargs["filename"]) 
        elif "image" in kwargs:
            self.image = kwargs["image"]


    def __del__(self):
        self.image.close()

