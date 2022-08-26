import cv2
import numpy as np


def compute_affine_transform(image_from: np.ndarray, image_to: np.ndarray):
    """
    computes and returns the affine transformation which maps parts of image_from to the corresponding parts on image_to
    images should be opened by cv2.imread
    """
    # image_from, image_to = (
    #     cv2.imread(image_from, cv2.IMREAD_GRAYSCALE),
    #     cv2.imread(image_to, cv2.IMREAD_GRAYSCALE),
    # )
    image_from = image_from.astype(np.uint8) * 255
    image_to = image_to.astype(np.uint8) * 255
    cv2.imshow("from", image_from)
    cv2.imshow("to", image_to)
    cv2.waitKey(0)

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
    keep = int(len(matches) * 0.9)
    matches = matches[:keep]
    print(len(matches))
    # check to see if we should visualize the matched keypoints
    if True:
        matchedVis = cv2.drawMatches(image_to, kpsA, image_from, kpsB, matches, None)
        cv2.imshow("Matched Keypoints", matchedVis)
        cv2.waitKey(0)
