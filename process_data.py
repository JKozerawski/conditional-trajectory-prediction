import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist
from matplotlib.patches import Circle
import pickle

from get_intersections import get_intersections
from get_map import image_to_city_coords, city_to_image_coords

class DataProcessor():
    def __init__(self):

        cities = ["MIA", "PIT"]
        self.intersection_coords = {}
        self.image_bounds = {}
        self.city_bounds = {}

        for city in cities:
            data = pickle.load(open("./"+city+"_info.p", "rb"))
            self.intersection_coords[city] = data[0]
            self.image_bounds[city] = data[1]
            self.city_bounds[city] = data[2]
            city_coords = []
            for i in range(len(data[0][0])):
                img_coords = data[0][:, i][::-1]

                city_coords_calc = image_to_city_coords(data[1], data[2], image_coords=img_coords)
                city_coords.append(city_coords_calc)
            city_coords = np.array(city_coords)
            #print(np.shape(city_coords))
            self.intersection_coords[city] = city_coords


    def process_data(self, dataset):
        # get inputs:
        inputs = dataset.input_data
        outputs = dataset.output_data
        helpers = dataset.helpers

        # get city information
        cities = [helpers[i][1][0] for i in range(len(helpers))]

        # get id information
        ids = [helpers[i][-1] for i in range(len(helpers))]

        # get necessary data here:
        distances, label = self.check_if_passed_intersection(inputs, outputs, cities)
        #data_in = self.check_if_passed_intersection(inputs, cities)
        #data_out = self.check_if_passed_intersection(outputs, cities)


        return distances, label #self.analyze_data(data_in, data_out)

    def get_closest_intersection(self, data, cities):
        assert len(data) == len(cities)
        info = []
        for i in range(len(data)):
            point = data[i, :, -1]
            x = self.intersection_coords[cities[i]][:, 0]
            y = self.intersection_coords[cities[i]][:, 1]
            dists = np.sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2)
            min_idx = np.argmin(dists)
            info.append([min_idx, dists[min_idx]])
        return np.asarray(info)

    def check_if_passed_intersection_old(self, data, cities):
        assert len(data) == len(cities)
        info = []
        for i in range(len(data)):
            #print(np.shape(self.intersection_coords[cities[i]]))
            x = self.intersection_coords[cities[i]][:, 0]
            y = self.intersection_coords[cities[i]][:, 1]
            temp_info = []
            for point in data[i]:
                dists = np.sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2)
                #print(np.shape(dists), np.shape(point), np.shape(x), np.shape(y))
                min_idx = np.argmin(dists)
                temp_info.append([min_idx, dists[min_idx]])
            temp_info = np.asarray(temp_info)
            info.append(temp_info)
        return np.asarray(info)

    def check_if_passed_intersection(self, data_in, data_out, cities):
        assert len(data_in) == len(cities)
        assert len(data_in) == len(data_out)
        info = []
        dist_threshold = 10
        passing = []
        for i in range(len(data_out)):
            #print(np.shape(self.intersection_coords[cities[i]]))
            x = self.intersection_coords[cities[i]][:, 0]
            y = self.intersection_coords[cities[i]][:, 1]
            temp_info = []
            for point in data_out[i]:
                dists = np.sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2)
                #print(np.shape(dists), np.shape(point), np.shape(x), np.shape(y))
                min_idx = int(np.argmin(dists))
                temp_info.append([min_idx, dists[min_idx]])
            temp_info = np.asarray(temp_info)
            min_idx = int(temp_info[np.argmin(temp_info[:, 1]), 0])  # closest intersection we have passed through
            if temp_info[np.argmin(temp_info[:, 1]), 1] <= dist_threshold:
                # passing through intersection
                passing.append(1)
            else:
                passing.append(0)

            temp_info = []
            for point in data_in[i]:
                distsX = (x - point[0])[min_idx]
                distsY = (y - point[1])[min_idx]

                temp_info.append([distsX, distsY])
            temp_info = np.asarray(temp_info)

            info.append(temp_info)
        return np.asarray(info), np.asarray(passing)


    def get_intersection_info(self, inputs, outputs):
        assert len(inputs) == len(outputs)
        single_intersections = []  # scenarios close to one intersection
        for i in range(len(outputs)):

            # check if always same intersection:
            unique_intersection_out = np.unique(outputs[i, :, 0])

            dist_threshold = 10

            if np.min(outputs[i, :, 1]) <= threshold:
                # we enter an intersection
                pass

            # check if we are getting closer or further away from intersections:

            # check if getting closer or further away
            min_idx = np.argmin(inputs[i, :, 1])
            if min_idx in [0, 1]:
                # we are getting away from intersection:
                pass
            elif min_idx in [len(inputs) - 2, len(inputs) - 1]:
                # we are getting closer to an intersection:
                pass
            if min_idx <= 0.25 * len(inputs[i]):
                pass
                # we are mostly getting away from intersection
            single_intersections.append([inputs[i, min_idx, 1], inputs[i, -1, 1]])

        return np.asarray(single_intersections)


    def analyze_data(self, inputs, outputs):

        assert len(inputs) == len(outputs)
        single_intersections = []   # scenarios close to one intersection
        for i in range(len(inputs)):

            # check if always same intersection:
            unique_intersection_in = np.unique(inputs[i, :, 0])
            unique_intersection_out = np.unique(outputs[i, :, 0])

            threshold = 20

            if np.min(inputs[i, :, 1]) <= threshold or np.min(outputs[i, :, 0]) <= threshold:
                # we might be close to intersection at some point
                pass

            # check if we are getting closer or further away from intersections:

            # check if getting closer or further away
            min_idx = np.argmin(inputs[i, :, 1])
            if min_idx in [0, 1]:
                # we are getting away from intersection:
                pass
            elif min_idx in [len(inputs)-2, len(inputs)-1]:
                # we are getting closer to an intersection:
                pass
            if min_idx <= 0.25*len(inputs[i]):
                pass
                # we are mostly getting away from intersection
            single_intersections.append([inputs[i, min_idx, 1], inputs[i, -1, 1]])

        return np.asarray(single_intersections)
