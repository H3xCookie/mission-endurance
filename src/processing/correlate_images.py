import cv2
import matplotlib.pyplot as plt
import numpy as np
from time_and_shoot.sat_image import SatImage


def compute_affine_transform(image_from_sat: SatImage, ground_image: SatImage):
    """ 
    computes and returns the affine transformation which maps parts of image_from to the corresponding parts on image_to
    images should be opened by cv2.imread and have one channel only, so shape (height, width)
    """
    # images should be 8 bit grayscale for detectAndCompute method
    image_from = image_from_sat.data.astype(np.uint8) * 255
    image_to = ground_image.data.astype(np.uint8) * 255

    max_features = 500
    orb = cv2.ORB_create(max_features)
    # print(image_from.shape, image_to.shape)
    # plt.imshow(image_from)
    # plt.show()
    (kpsA, descsA) = orb.detectAndCompute(image_to, None)
    (kpsB, descsB) = orb.detectAndCompute(image_from, None)

    # match the features
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descsA, descsB, None)

    matches = sorted(matches, key=lambda x: x.distance)
    print(kpsB[:5])

    # keep only the top matches
    keep = int(len(matches) * 0.8)
    matches = matches[:keep]
    n_matches = len(matches)
    print(f"Number of matches: {n_matches}")
    if False:
        matchedVis = cv2.drawMatches(
            image_to, kpsA, image_from, kpsB, matches[:30], None
        )
        plt.imshow(matchedVis)
        plt.show()

    p1 = np.zeros((n_matches, 2))
    p2 = np.zeros((n_matches, 2))

    for i in range(len(matches)):
        p1[i, :] = kpsA[matches[i].queryIdx].pt
        p2[i, :] = kpsB[matches[i].trainIdx].pt

    homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC)
    return homography

def get_ksts_decriptors(coastline: SatImage):
    coastline_data = coastline.data.astype(np.uint8) * 255

    max_features = 500
    orb = cv2.ORB_create(max_features)
    (kpsA, descsA) = orb.detectAndCompute(coastline_data, None)
    return (kpsA, descsA)
