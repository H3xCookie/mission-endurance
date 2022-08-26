import cv2
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans


def b_index(bgr):
    return 2 * int(bgr[0]) - int(bgr[1]) - int(bgr[2])


def compute_coastline(image_filename, csv=False):
    """
    Computes the coastline of the image. If csv=False, returns a black and white image mask, i.e. black is coastline, white is not
    """
    image: np.ndarray = cv2.imread(image_filename)
    height, width, _ = image.shape

    flat_data = image.reshape((width * height, 3))
    blue_values = np.array([b_index(pixel) for pixel in flat_data])
    plt.hist(blue_values, bins=100)
    plt.show()

    in_sea = blue_values > 130
    final = in_sea.reshape((height, width))
    # model = KMeans(n_clusters=2, max_iter=30)
    # labels = model.fit_predict(flat_data)
    # print(labels.shape)
    # new_image = labels.reshape((height, width))
    plt.imshow(final)
    plt.show()

    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # filter_size = int(0.05 * (width + height) / 2)
    # img_blur = cv2.GaussianBlur(gray_image, (filter_size, filter_size), 0)
    # edges = cv2.Canny(
    #     image=gray_image, threshold1=250, threshold2=255
    # )  # Canny Edge Detection
    # # Display Canny Edge Detection Image
    # cv2.imshow("Blur", img_blur)
    # cv2.imshow("Canny Edge Detection", edges)
    # cv2.waitKey(0)
