import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np


class Cluster():
    def __init__(self):
        self.average = None
        self.points = []

def get_distance(p0, p1):
    """Returns the distance between two 2d points"""
    return np.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def calc_average_cluster(points):
    """Returns the average point of a group of 2d cluster points"""
    return [sum([p[0] for p in points])/len(points),sum([p[1] for p in points])/len(points)]


def classify_point(p, cluster_averages):
    """Classifies a point based on which cluster's average it is closest to.

    Returns the index of the cluster_averages of which it's closest to"""
    distance_from_cluster_averages = [get_distance(p, cluster_average) for cluster_average in cluster_averages]
    return distance_from_cluster_averages.index(min(distance_from_cluster_averages))

def create_new_clusters(data_set, cluster_averages):
    """Classifies all the points in the dataset, returns all the new clusters"""
    new_clusters = []
    for i in range(len(cluster_averages)):
        new_clusters.append([])
    for p in data_set:
        p_classification = classify_point(p, cluster_averages)
        new_clusters[p_classification].append(p)
    return new_clusters

def main():
    with open(r"../Input_Files/GMM_dataset 546.txt") as f:
        data_set = [[float(num.replace(',', '.')) for num in line.split()] for line in f]



if __name__ == "__main__":
    main()