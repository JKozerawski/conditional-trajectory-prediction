import pickle
import matplotlib.pyplot as plt
import numpy as np
import random
from get_intersections import get_intersections
from get_map import get_mapping, image_to_city_coords, city_to_image_coords
# goal compare output of get_intersection with any coordinate (x,y) pair in any of the out/input pkl files
# task is  to create a function that given any 2d point (x,y), find the closest intersection
class dictionary: 
    def __init__(self, sq_id) -> None:
        self.city = None
        self.sequence_id = sq_id
        self.ground_truth = None
        self.trajectories = None
        self.performance = None
      
    def set_ground_truth(self, gt):
        self.ground_truth = gt

    def set_trajectories(self, tj):
        self.trajectories = tj[0]

    def set_city(self, ct):
        self.city = ct

    def set_input(self, ip):
        self.input = ip
    
    def set_performance(self, pf):
        self.performance = pf

    def get_id(self):
        return self.sequence_id
        

def get_pickle_data(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data

def get_dictionary(metric_type):
    city_train_data = get_pickle_data('data/ground_truth_data/city_train.pkl')
    input_train_data = get_pickle_data('data/ground_truth_data/input_train.pkl')
    ground_truth_train_data = get_pickle_data('data/ground_truth_data/ground_truth_train.pkl')
    trajectories_train_data = get_pickle_data('data/trajectories/traj_train.pkl')
    performance_data = get_pickle_data('data/performance/lstm_performance_train.p')
    keys = city_train_data.keys()
    dc = {}
    for key in keys:
        dc[key] = dictionary(key)
        dc[key].set_ground_truth(ground_truth_train_data[key])
        dc[key].set_trajectories(trajectories_train_data[key])
        dc[key].set_city(city_train_data[key])
        dc[key].set_input(input_train_data[key])
        dc[key].set_performance(performance_data[metric_type][key])
    return list(keys), dc

def plot_sequence(sequence, cl, ax):
    ax.plot(
        sequence[:, 0],
        sequence[:, 1],
        "--",
        color=cl,
        alpha=1,
        linewidth=3,
        zorder=0,
    )

def get_dist_closest_intersection(inter_coords, sequence):

    x = inter_coords[:, 0]
    y = inter_coords[:, 1]
    point = sequence[-1]
    min_dist = np.min(np.sqrt((x - point[0])**2 + (y - point[1])**2))
    return min_dist

def get_coordinate_closest_intersection(inter_coords, sequence):
    x = inter_coords[:, 0]
    y = inter_coords[:, 1]
    point = sequence[-1]
    min_coor_inx = np.argmin(np.sqrt((x - point[0])**2 + (y - point[1])**2))
    return min_coor_inx 


def get_direction(inter_coords, sequence):

    min_coor_inx = get_coordinate_closest_intersection(inter_coords, sequence)
    x = inter_coords[min_coor_inx, 0]
    y = inter_coords[min_coor_inx, 1]
    dists = []
    for point in sequence:
        dist = np.sqrt((x - point[0])**2 + (y - point[1])**2)
        dists.append(dist)
    gradient = np.gradient(dists)
    gradient_positive = len(np.argwhere(gradient > 0))
    gradient_negative = len(np.argwhere(gradient < 0))
    if gradient_positive > 0 and gradient_negative == 0:
        return "AWAY"
    elif gradient_negative > 0 and gradient_positive == 0:
        return "CLOSER"
    else:
        return "NOT SURE"


def print_info(key, dc):
    print("sequence id: ", dc[key].sequence_id)
    print(dc[key].city)
    fig, ax = plt.subplots()
    plot_sequence(dc[key].input, "black", ax)
    plot_sequence(dc[key].ground_truth, "red", ax)
    plot_sequence(dc[key].trajectories, "blue", ax)
    plt.show()

def visualize_each_scene(city_name):
    if city_name == "PIT":
        labeled_image_path = "./map_PIT_labeled.png"
    elif city_name == "MIA":
        labeled_image_path = "./map_MIA_labeled.png"
    keys, dc = get_dictionary(metric_type='ade')
    index = random.randint(0, len(keys))
    test_key = keys[index]
    print_info(test_key, dc)
    labeled_image_path = "./map_MIA_labeled.png"
    intersection_image, intersection_coords = get_intersections(image_path=labeled_image_path)
    dist = get_dist_closest_intersection(intersection_coords, dc[test_key].input)
    print("Closest distance to intersection is: ", dist)

def get_intersection_coordinates(city_name):
    if city_name == "PIT":
        labeled_image_path = "./map_PIT_labeled.png"
    elif city_name == "MIA":
        labeled_image_path = "./map_MIA_labeled.png"
    intersection_image, inter_coords = get_intersections(image_path=labeled_image_path)
    image_bounds, city_bounds = get_mapping(city_name)
    city_coords = []
    for i in range(len(inter_coords[0])):
        img_coords = inter_coords[:, i][::-1]
        city_coords_calc = image_to_city_coords(image_bounds, city_bounds, image_coords=img_coords)
        city_coords.append(city_coords_calc)
    city_coords = np.array(city_coords)
    return city_coords

def plot_performance(metric_type, city_name, option="NONE", data_type="INPUT"):
    fig, ax = plt.subplots()
    inter_coords = get_intersection_coordinates(city_name)
    keys, dc = get_dictionary(metric_type)
    dists = []
    pfs = []
    for key in keys:
        if data_type == "OUTPUT":
            data = dc[key].trajectories
        else:
            data = dc[key].input
    
        if dc[key].city == city_name and (option == "NONE" or get_direction(inter_coords, data) == option):
            dists.append(get_dist_closest_intersection(inter_coords, data))
            pfs.append(dc[key].performance)
    ax.scatter(dists, pfs, s=1)
    ax.set(xlabel="distance to closest intersection", ylabel=metric_type)
    title = city_name
    if option == "AWAY":
        title += " away from intersection"
    elif option == "CLOSER":
        title += " closer to intersection"
    if data_type == "INPUT":
        title += " (INPUT)"
    elif data_type == "OUTPUT":
        title += " (OUTPUT)"
    
    ax.set_title(title)
    plt.show()

#visualize_each_scene()
plot_performance(metric_type='ade', city_name="MIA")
plot_performance(metric_type='fde', city_name="MIA")
plot_performance(metric_type='ade', city_name="MIA", option="AWAY")
plot_performance(metric_type='fde', city_name="MIA", option="AWAY")
plot_performance(metric_type='ade', city_name="MIA", option="CLOSER")
plot_performance(metric_type='fde', city_name="MIA", option="CLOSER")
#plot_performance(metric_type='ade', city_name="MIA", data_type="OUTPUT")
#plot_performance(metric_type='fde', city_name="MIA", data_type="OUTPUT")
plot_performance(metric_type='ade', city_name="PIT")
plot_performance(metric_type='fde', city_name="PIT")
plot_performance(metric_type='ade', city_name="PIT", option="AWAY")
plot_performance(metric_type='fde', city_name="PIT", option="AWAY")
plot_performance(metric_type='ade', city_name="PIT", option="CLOSER")
plot_performance(metric_type='fde', city_name="PIT", option="CLOSER")
#plot_performance(metric_type='ade', city_name="PIT", data_type="OUTPUT")
#plot_performance(metric_type='fde', city_name="PIT", data_type="OUTPUT")