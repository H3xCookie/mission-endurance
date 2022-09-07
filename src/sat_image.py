import cv2
import numpy as np


class SatImage:
    def __init__(self, filename=None, image=None, **kwargs):
        """
        pass either filename= or an image= read by cv2, so an np.ndarray, and optionally a mask=np.ndarray of bools, where True is useable land, and False meand the pixel is a cloud. The bands in the data np.ndarray should be of shape (height, width, 3), and in order B, G, R
        """
        if filename is None and image is None:
            print("specify either image=cv2.imread or filename=<fullpath>.tif")
        if not (filename is None):
            self.data: np.ndarray = cv2.imread(filename)
        elif not (image is None):
            self.data: np.ndarray = image
        if "cloud_mask" in kwargs:
            self.mask = kwargs["cloud_mask"]
        else:
            self.mask = np.full(self.data.shape, True)
