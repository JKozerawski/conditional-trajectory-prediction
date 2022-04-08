"""
File to find mapping between image and city coordinates
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from argoverse.map_representation.map_api import ArgoverseMap
avm = ArgoverseMap()
seq_lane_props_cities = dict()
seq_lane_props_cities["MIA"] = avm.city_lane_centerlines_dict["MIA"]
seq_lane_props_cities["PIT"] = avm.city_lane_centerlines_dict["PIT"]


def save_map(city_name="MIA"):
    matplotlib.rcParams['figure.dpi'] = 300
    matplotlib.rcParams['savefig.dpi'] = 300
    seq_lane_props = seq_lane_props_cities[city_name]
    fig, ax = plt.subplots()

    lane_centerlines = []
    # Get lane centerlines which lie within the range of trajectories
    for lane_id, lane_props in seq_lane_props.items():
        lane_cl = lane_props.centerline
        lane_centerlines.append(lane_cl)

    x_min, y_min, x_max, y_max = 10000, 10000, -1000000, -1000000

    for lane_cl in lane_centerlines:
        plt.plot(
            lane_cl[:, 0],
            lane_cl[:, 1],
            "-",
            color="b",
            alpha=1,
            linewidth=5,
            zorder=0
        )
        if np.min(lane_cl[:, 0]) < x_min:
            x_min = np.min(lane_cl[:, 0])
        if np.max(lane_cl[:, 0]) > x_max:
            x_max = np.max(lane_cl[:, 0])
        if np.min(lane_cl[:, 1]) < y_min:
            y_min = np.min(lane_cl[:, 1])
        if np.max(lane_cl[:, 1]) > y_max:
            y_max = np.max(lane_cl[:, 1])

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    print(x_min, y_min, x_max, y_max)
    #ax.autoscale()

    ax.axis('equal')

    #plt.axis("off")
    plt.show()
    #plt.savefig("./map_" + city_name + ".png", format='png')

def get_city_bounds(city_name="MIA"):
    seq_lane_props = seq_lane_props_cities[city_name]

    lane_centerlines = []
    # Get lane centerlines which lie within the range of trajectories
    for lane_id, lane_props in seq_lane_props.items():
        lane_cl = lane_props.centerline
        lane_centerlines.append(lane_cl)

    x_min, y_min, x_max, y_max = 10000, 10000, -1000000, -1000000

    for lane_cl in lane_centerlines:
        if np.min(lane_cl[:, 0]) < x_min:
            x_min = np.min(lane_cl[:, 0])
        if np.max(lane_cl[:, 0]) > x_max:
            x_max = np.max(lane_cl[:, 0])
        if np.min(lane_cl[:, 1]) < y_min:
            y_min = np.min(lane_cl[:, 1])
        if np.max(lane_cl[:, 1]) > y_max:
            y_max = np.max(lane_cl[:, 1])
    return x_min, y_min, x_max, y_max


def get_img_bounds(city_name="MIA"):
    if city_name == "MIA":
        image_path = "./map_" + city_name + "_labeled.png"
    elif city_name == "PIT":
        image_path = "./map_" + city_name + "_labeled.png"
    else:
        print("Wrong city used")

    labeled = matplotlib.image.imread(image_path)
    labeled = np.array(labeled)[:, :, :3]
    img_dims = np.shape(labeled)
    # get dimensions:
    if city_name == "PIT":
        for i in range(img_dims[0]):

            if np.sum(labeled[i, ...]) < 3*img_dims[1]:
                y_min = i
                break
        for i in range(img_dims[0]-1, 0, -1):
            if np.sum(labeled[i, ...]) < 3*img_dims[1]:
                y_max = i
                break
        for i in range(img_dims[1]):
            if np.sum(labeled[:,i, ...]) < 3*img_dims[0]:
                x_min = i
                break
        for i in range(img_dims[1]-1, 0, -1):
            if np.sum(labeled[:, i, ...]) < 3*img_dims[0]:
                x_max = i
                break
    elif city_name == "MIA":
        for i in range(img_dims[0]):
            if np.sum(labeled[i, ...]) > 0:
                y_min = i
                break
        for i in range(img_dims[0]-1, 0, -1):
            if np.sum(labeled[i, ...]) > 0:
                y_max = i
                break
        for i in range(img_dims[1]):
            if np.sum(labeled[:,i, ...]) > 0:
                x_min = i
                break
        for i in range(img_dims[1]-1, 0, -1):
            if np.sum(labeled[:, i, ...]) > 0:
                x_max = i
                break

    return x_min, y_min, x_max, y_max

def check_coordinates(bounds, coords):

    assert coords[0] >= bounds[0]
    assert coords[1] >= bounds[1]
    assert coords[0] <= bounds[2]
    assert coords[1] <= bounds[3]

def city_to_image_coords(image_bounds, city_bounds, city_coords):

    # city coords have to be within city bounds:
    check_coordinates(city_bounds,city_coords)

    city_width = city_bounds[2] - city_bounds[0]
    city_height = city_bounds[3] - city_bounds[1]

    image_width = image_bounds[2] - image_bounds[0]
    image_height = image_bounds[3] - image_bounds[1]

    image_coords = np.zeros(2)
    image_coords[0] = image_bounds[0] + image_width * (city_coords[0] - city_bounds[0])/city_width
    image_coords[1] = image_bounds[1] + image_height * (city_bounds[3] - city_coords[1]) / city_height
    #image_coords[1] = image_bounds[1] + image_height * (city_coords[1] - city_bounds[1]) / city_height

    # check if valid image coordinates:
    check_coordinates(image_bounds, image_coords)

    return image_coords

def image_to_city_coords(image_bounds, city_bounds, image_coords):

    # city coords have to be within city bounds:
    check_coordinates(image_bounds, image_coords)

    city_width = city_bounds[2] - city_bounds[0]
    city_height = city_bounds[3] - city_bounds[1]

    image_width = image_bounds[2] - image_bounds[0]
    image_height = image_bounds[3] - image_bounds[1]

    city_coords = np.zeros(2)
    city_coords[0] = city_bounds[0] + city_width * (image_coords[0] - image_bounds[0])/image_width
    city_coords[1] = city_bounds[1] + city_height * (image_bounds[3] - image_coords[1]) / image_height

    # check if valid image coordinates:
    check_coordinates(city_bounds, city_coords)

    return city_coords

def get_mapping(city_name="MIA"):
    image_bounds = get_img_bounds(city_name)
    city_bounds = get_city_bounds(city_name)


    return image_bounds, city_bounds

if __name__=="__main__":
    image_bounds, city_bounds = get_mapping(city_name="MIA")
