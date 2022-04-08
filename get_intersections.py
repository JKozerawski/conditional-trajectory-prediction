"""
File to find the intersections (in image coordinates)
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist
from matplotlib.patches import Circle

def get_intersections(image_path):
    labeled = matplotlib.image.imread(image_path)


    if labeled.shape[2] == 4:
        # Miami
        labeled = np.array(labeled)[:, :, :3]
        image = get_only_red(labeled)
    else:
        # Pittsburgh
        labeled = np.abs(np.asarray(labeled)-np.max(labeled))
        image = labeled
        image[:, :, 0] *= 0
        image[:, :, 1] *= 0
        image[:, :, 0] = image[:, :, 2]
        image[:, :, 2] *= 0

    indices = get_red_indices(image, threshold=0.1)
    intersection_coords = get_xy_intersections(indices, threshold=25)
    intersection_image = get_intersection_image(image, intersection_coords)
    return intersection_image, intersection_coords

def get_only_red(image):
    image[:, :, 1:] *= 0
    return image

def get_red_indices(image, threshold):
    indices = np.where(image[:, :, 0] >= threshold)
    return indices

def get_intersection_image(image, indices):
    image *= 0
    for i in range(len(indices[0])):
        image[indices[1, i], indices[0, i], 0] = 1
    return image

def get_xy_intersections(indices, threshold=10):
    indices = np.transpose(indices)
    new_groups = []
    while len(indices) > 0:
        b = cdist(indices, np.expand_dims(indices[0], axis=0))
        c = np.where(b < threshold)[0]
        if (len(c) != 0):
            new_groups.append(np.mean(indices[c], axis=0))
            indices = np.delete(indices, c, axis=0)
    return np.transpose(np.asarray(new_groups)).astype(int)