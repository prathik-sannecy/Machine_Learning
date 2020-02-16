# This file implements GMM algorithm on a set of 2d data points (GMM_dataset 546.txt in this case).
# The number of clusters (k), can be set by defining the k_values parameter below.
# If many k_values are chosen, the one with the highest k is plotted.
# Written by Prathik Sannecy
# 2/15/2020

import Programming_Assignment1.Source.kMeans as kMeans
import numpy as np
from scipy.stats import norm, multivariate_normal
import math
import matplotlib.pyplot as plt
from matplotlib import style

num_runs = 100 # number of runs to try clustering on. Chooses the best clustering based on which run had the least error
k_values = [5] # which k values to run kmeans on
tolerance = .1 # tolerance for when to stop the algorithm (based on log-likelyhood)

def initialize_GMM(data_set, k):
    """Run kMeans to initialize the centroids, the covariances (x and y coordinates per data point), the the pi values for the GMM algorithm"""
    global num_runs
    init_centroids = kMeans.initialize_centroids(data_set, k)
    init_clusters, init_centroids = kMeans.run_kmeans(data_set, init_centroids)
    init_cov = [np.cov([point[0] for point in cluster], [point[1] for point in cluster]).tolist() for cluster in init_clusters]
    init_pi = [len(cluster) / len(data_set) for cluster in init_clusters]
    assert(sum(init_pi) == 1)
    return init_centroids, init_cov, init_pi

def e_step(data_set, centroids, cov, pi, k):
    """Runs the E Step of the GMM algorithm, and returns gamma
    gamma = pi_k * N(x_n|centroid_k, cov_k) / (Sum from j = 1 to K(pi_j * N(x_n|centroid_j, cov_j))
    """
    # gamma is a num of clusters x num of datapoints size 2D matrix
    gamma = [[0]*len(data_set) for _ in range(k)]
    # Calculate the numerator of gamma
    for cluster_data_set_index in range(k):
        for i in range(len(data_set)):
            var = multivariate_normal(centroids[cluster_data_set_index], cov[cluster_data_set_index])
            var_pdf = var.pdf(data_set[i])
            gamma[cluster_data_set_index][i] = pi[cluster_data_set_index] * var_pdf
    # Calculate the denominator of gamma
    datapoint_normalization = []
    for i in range(len(data_set)):
        datapoint_normalization.append(sum([cluster[i] for cluster in gamma]))
    # Normalize gamma by dividing each element by the denominator
    for cluster_data_set_index in range(k):
        for i in range(len(data_set)):
            gamma[cluster_data_set_index][i] /= datapoint_normalization[i]
    return gamma

def m_step(data_set, gamma):
    """Runs the M Step of the GMM algorithm, and returns the new centroids, covariances, and pi values
    centroidNew_k = (1/N_k) * Sum from n = 1 to N(gamma_k_n * x_n)
    covarianceNew_k = (1/N_k) * Sum from n = 1 to N(gamma_k_n * (x_n - centroidNew_k) * (x_n - centroidNew_k)^T))
    piNew_k = N_k / N
    """
    Nk = [sum(gamma_cluster) for gamma_cluster in gamma] # Normalization factor
    centroids_new = []
    # Calculate the centroid of each cluster
    for cluster_data_set_index in range(len(gamma)):
        cluster_mean_x = 0
        cluster_mean_y = 0
        for i in range(len(data_set)):
            cluster_mean_x += gamma[cluster_data_set_index][i]*data_set[i][0]
            cluster_mean_y += gamma[cluster_data_set_index][i]*data_set[i][1]
        cluster_mean_x /= Nk[cluster_data_set_index]
        cluster_mean_y /= Nk[cluster_data_set_index]
        centroids_new.append([cluster_mean_x, cluster_mean_y])
    # Calculate the covariance of each cluster
    cov_new = []
    for cluster_data_set_index in range(len(gamma)):
        cov_xx = 0
        cov_yy = 0
        cov_xy = 0
        for i in range(len(data_set)):
            cov_xx += (1/Nk[cluster_data_set_index])*gamma[cluster_data_set_index][i]*(data_set[i][0] - centroids_new[cluster_data_set_index][0])**2
            cov_yy += (1/Nk[cluster_data_set_index])*gamma[cluster_data_set_index][i]*(data_set[i][1] - centroids_new[cluster_data_set_index][1])**2
            cov_xy += (1/Nk[cluster_data_set_index])*gamma[cluster_data_set_index][i]*(data_set[i][1] - centroids_new[cluster_data_set_index][1])*(data_set[i][0] - centroids_new[cluster_data_set_index][0])
        cov_new.append([[cov_xx, cov_xy], [cov_xy, cov_yy]])

    pi_new = [Nk_cluster/len(data_set) for Nk_cluster in Nk] # Calculate the new pi value for each cluster
    return centroids_new, cov_new, pi_new

def calc_log_likelyhood(data_set, centroids, cov, pi):
    """Calculates log(p(X|centroids, covariances, pi values)) =
        Sum from n=1 to N(log(Sum from k=1 to K(pi_k * N(x_n|centroids_k, covariances_k))))"""
    sum_likelyhoods = 0
    for i in range(len(data_set)):
        sum_cluster = 0
        for cluster_data_set_index in range(len(pi)):
            var = multivariate_normal(centroids[cluster_data_set_index], cov[cluster_data_set_index])
            var_pdf = var.pdf(data_set[i])
            sum_cluster += pi[cluster_data_set_index] * var_pdf
        sum_likelyhoods += math.log(sum_cluster)
    return sum_likelyhoods


def classify(data_set, gamma):
    """Based on the gamma function, classifies the points into cluster.
    Basically, the point gets classified into the cluster that has the largest gamma function for that point
    Then display the scatter plot of the clusters
    """
    clusters = [[] for _ in gamma]
    # For each point, search the gamma function cluster indexes for the maximum value. Add that point to that cluster
    for i in range(len(data_set)):
        clusters_with_i = [cluster[i] for cluster in gamma]
        max_cluster_with_i = clusters_with_i.index(max(clusters_with_i))
        clusters[max_cluster_with_i].append(data_set[i])

    colors = 10 * ["r", "g", "c", "b", "k"]
    for cluster_index in range(len(clusters)):
        color = colors[cluster_index]
        for features in clusters[cluster_index]:
            plt.scatter(features[0], features[1], color=color, s=30)

    plt.show()

def main():
    global k_values
    global num_runs
    global tolerance
    log_likelyhood_old = float("-inf")
    data_set = kMeans.get_data_set(r"../Input_Files/GMM_dataset 546.txt")
    initial_centroids, init_cov, init_pi = initialize_GMM(data_set, k_values[0])

    # Run at least 1 iteration of GMM
    gamma = e_step(data_set, initial_centroids, init_cov, init_pi, k_values[0])
    centroids, cov, pi = m_step(data_set, gamma)
    log_likelyhood = calc_log_likelyhood(data_set, centroids, cov, pi)
    count = 1

    # Go until we've reached the max number of iterations, or we've converged (log-likelyhood isn't changing)
    while log_likelyhood > (log_likelyhood_old + tolerance):
        if count >= num_runs:
            break
        gamma = e_step(data_set, centroids, cov, pi, k_values[0])
        centroids, cov, pi = m_step(data_set, gamma)
        log_likelyhood_old = log_likelyhood
        log_likelyhood = calc_log_likelyhood(data_set, centroids, cov, pi)
        count += 1
        print(log_likelyhood)

    classify(data_set, gamma) # Classify the points based on their gamma functions

if __name__ == "__main__":
    main()