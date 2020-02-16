# This file implements kMeans algorithm on a set of 2d data points (GMM_dataset 546.txt in this case).
# The number of clusters (k), can be set by defining the k_values parameter below.
# If many k_values are chosen, the one with the highest k is plotted.
# Written by Prathik Sannecy
# 2/15/2020


import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import random

num_runs = 10 # number of runs to try clustering on. Chooses the best clustering based on which run had the least error
k_values = [3] # which k values to run kmeans on

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

def get_new_averages(clusters):
    """Returns the centroids/averages of each cluster of data points"""
    return [calc_average_cluster(cluster) for cluster in clusters]

def get_data_set(data_set_file):
    """Parses a text file of 2d data points, returns a list of list of data points"""
    with open(data_set_file) as f:
        data_set = [[float(num.replace(',', '.')) for num in line.split()] for line in f]
    return data_set

def initialize_centroids(data_set, k):
    """Uses a random set of k points of the data set as the initial centroids of the clusters"""
    return [data_set[int(random.random() * len(data_set))] for i in range(k)]

def run_kmeans(data_set, initial_centroids, r=None):
    """Runs kmeans using k clusters for r iterations (or until centroids don't change)
    Returns the clusters, and the cluster averages"""
    old_centroids = initial_centroids[:]
    # Run the iteration at least once
    clusters = create_new_clusters(data_set, old_centroids)
    centroids = get_new_averages(clusters)
    i = 1
    while centroids != old_centroids: # Run until the centroids don't change
        # If set number of iterations
        if r != None:
            if i>= r:
                break
        old_centroids = centroids[:]
        clusters = create_new_clusters(data_set, centroids)
        centroids = get_new_averages(clusters)
        i += 1
    return clusters, centroids

def get_error_squared(p0, p1):
    """Returns the squared error between two 2d points"""
    return (p0[0] - p1[0])**2 + (p0[1] - p1[1])**2

def calc_clusters_error(clusters, centroids):
    """Returns the total error of a certain clustering of data points"""
    error = 0
    for cluster_index in range(len(centroids)):
        for p in clusters[cluster_index]:
            error += get_error_squared(p, centroids[cluster_index])
    return error

def get_best_kmeans(data_set, r, k ):
    """Runs kMeans with k clusters r number of times. Returns the best clustering from those r runs, and the squared error of the resulting clustering"""
    runs_centroids = []
    runs_clusters = []
    min_run_error = float("inf")

    for run in range(r):
        initial_averages = initialize_centroids(data_set, k)
        clusters, centroids = run_kmeans(data_set, initial_averages)
        run_error = calc_clusters_error(clusters, centroids)
        # Keep track of the best run
        if run_error < min_run_error:
            min_run_error = run_error
            best_clusturing = clusters
    return best_clusturing, min_run_error

def main():
    global num_runs
    global k_values

    data_set = get_data_set(r"../Input_Files/GMM_dataset 546.txt")

    # Run the kmeans algorithms with different values of k
    min_kmean_error = float("inf")
    for k in k_values:
        clusters, error = get_best_kmeans(data_set, num_runs, k)
        print("number of clusters: "+ str(k) + "; clustering error:" + str(error))
        # Keep track of which value of k gives the smallest error
        if error < min_kmean_error:
            best_kmeans_clustering_model = clusters
            min_kmean_error = error


    # Display the kMeans clusters in a scatter plot
    colors = 10 * ["r", "g", "c", "b", "k"]
    for cluster_index in range(len(best_kmeans_clustering_model)):
        color = colors[cluster_index]
        for features in best_kmeans_clustering_model[cluster_index]:
            plt.scatter(features[0], features[1], color=color, s=30)

    plt.show()

if __name__ == "__main__":
    main()