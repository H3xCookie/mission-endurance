import cv2
import matplotlib.pyplot as plt
import numpy as np
from time_and_shoot.sat_image import SatImage

class Keypoints:
    def __init__(self, shape, kpts, desc):
        self.shape = shape
        self.kpts = kpts
        self.desc = desc

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


def compute_transform_from_keypoints(sat_keypoints: Keypoints, ground_keypoints: Keypoints):
    """ 
    computes and returns the affine transformation which maps parts of image_from to the corresponding parts on image_to
    images should be opened by cv2.imread and have one channel only, so shape (height, width)
    """
    # match the features
    kpsA, descA = sat_keypoints.kpts, sat_keypoints.desc
    kpsB, descB = ground_keypoints.kpts, ground_keypoints.desc
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descA, descB, None)

    matches = sorted(matches, key=lambda x: x.distance)

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
    

def get_keypoints(coastline: SatImage) -> Keypoints:
    coastline_data = coastline.data.astype(np.uint8) * 255

    max_features = 500
    orb = cv2.ORB_create(max_features)
    (kpsA, descsA) = orb.detectAndCompute(coastline_data, None)
    return Keypoints(coastline_data.shape, kpsA, descsA) 
