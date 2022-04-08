"""
Main file
"""

import matplotlib
import argparse
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist
from matplotlib.patches import Circle

from get_intersections import get_intersections
from get_map import save_map, get_mapping, image_to_city_coords, city_to_image_coords
from show_plots import plot_performance


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--city",
        required=False,
        type=str,
        help=
        "city name",
    )
    args = parser.parse_args()

    city = args.city


    labeled_image_path = "./map_"+city+"_labeled.png"
    intersection_image, intersection_coords = get_intersections(image_path=labeled_image_path)
    print("Got intersections", np.shape(intersection_coords))
    # At this point intersection image has a single red pixel per intersection

    image_bounds, city_bounds = get_mapping(city_name=city)
    print(image_bounds, city_bounds)
    #save_map(city_name=city)

    plot_performance('ade', city, intersection_coords, image_bounds, city_bounds)


    # This is just for visualization (just to enhance that view):
    '''fig, ax = plt.subplots(1, 2)
    #plt.imshow(intersection_image)
    print(image_bounds, city_bounds)
    # Sanity check if the coordinate conversion works:
    a = image_to_city_coords(image_bounds, city_bounds, image_coords=np.asarray([image_bounds[0], image_bounds[1]]))
    a = image_to_city_coords(image_bounds, city_bounds, image_coords=np.asarray([image_bounds[2], image_bounds[3]]))


    for i in range(len(intersection_coords[0])):
        img_coords = intersection_coords[:, i][::-1]
        city_coords_calc = image_to_city_coords(image_bounds, city_bounds, image_coords=img_coords)
        img_coords_calc = city_to_image_coords(image_bounds, city_bounds, city_coords=city_coords_calc)
        #print(img_coords, img_coords_calc)
        #print(intersection_coords[1, i], intersection_coords[0, i])
        ax[0].scatter(intersection_coords[1, i], intersection_coords[0, i], s=10, c='b')
        ax[1].scatter(city_coords_calc[0], city_coords_calc[1], s=10, c='r')
        #plt.scatter(intersection_coords[1, i], intersection_coords[0, i], s=10, c='b')
        #circ = Circle((intersection_coords[1, i], intersection_coords[0, i]), 25)
        #ax.add_patch(circ)
    ax[0].axis('equal')
    ax[1].axis('equal')
    plt.show()'''
