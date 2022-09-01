import cv2
import numpy as np


class SatImage:
    def __init__(self, **kwargs):
        """
        pass either filename= or an image= read by cv2, so an np.ndarray
        """
        if "image" not in kwargs and "filename" not in kwargs:
            print("specify either image=cv2.imread or filename=<fullpath>.tif")
        if "filename" in kwargs:
            self.data: np.ndarray = cv2.imread(kwargs["filename"])
        elif "image" in kwargs:
            self.data: np.ndarray = kwargs["image"]
        if "cloud_mask" in kwargs:
            self.mask = kwargs["cloud_mask"]
        else:
            self.mask = np.full(self.data.shape, True)
