import cv2
import numpy as np


def compute_affine_transform(image_from: np.ndarray, image_to: np.ndarray):
    """
    computes and returns the affine transformation which maps parts of image_from to the corresponding parts on image_to
    images should be opened by cv2.imread
    """
    image_from = image_from.astype(np.uint8) * 255
    image_to = image_to.astype(np.uint8) * 255

    max_features = 500
    orb = cv2.ORB_create(max_features)
    (kpsA, descsA) = orb.detectAndCompute(image_to, None)
    (kpsB, descsB) = orb.detectAndCompute(image_from, None)

    # match the features
    method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
    matcher = cv2.DescriptorMatcher_create(method)
    matches = matcher.match(descsA, descsB, None)

    matches = sorted(matches, key=lambda x: x.distance)
    # keep only the top matches
    keep = int(len(matches) * 0.8)
    matches = matches[:keep]
    n_matches = len(matches)
    print(f"Number of matches: {n_matches}")
    if False:
        matchedVis = cv2.drawMatches(image_to, kpsA, image_from, kpsB, matches, None)
        cv2.imshow("Matched Keypoints", matchedVis)
        cv2.waitKey(0)

    p1 = np.zeros((n_matches, 2))
    p2 = np.zeros((n_matches, 2))

    for i in range(len(matches)):
        p1[i, :] = kpsA[matches[i].queryIdx].pt
        p2[i, :] = kpsB[matches[i].trainIdx].pt

    homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC)
    return homography
