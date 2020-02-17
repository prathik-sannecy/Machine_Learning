# This file implements GMM algorithm on a set of 2d data points (GMM_dataset 546.txt in this case).
# The number of clusters (k), can be set by defining the k_values parameter below.
# If many k_values are chosen, the one with the highest k is plotted.
# Written by Prathik Sannecy
# 2/15/2020

import kMeans
import numpy as np
from scipy.stats import norm, multivariate_normal
import math
import matplotlib.pyplot as plt
from matplotlib import style

file_name = r"../Input_Files/GMM_dataset 546.txt" # file with the data set
k_values = [3] # which k values to run kmeans on
num_runs = 5 # number of runs to try clustering on. Chooses the best clustering based on which run had the least error
tolerance = .1 # tolerance for when to stop the algorithm (based on log-likelyhood)
max_iterations = 100 # In case this algorithm doesn't converge, stop after this many iterations

def initialize_GMM(data_set, k):
    """Run kMeans to initialize the centroids, the covariances (x and y coordinates per data point), the the pi values for the GMM algorithm"""
    init_centroids = kMeans.initialize_centroids(data_set, k)
    init_clusters, init_centroids = kMeans.run_kmeans(data_set, init_centroids)
    init_cov = [np.cov([point[0] for point in cluster], [point[1] for point in cluster]).tolist() for cluster in init_clusters]
    init_pi = [len(cluster) / len(data_set) for cluster in init_clusters]
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

def run_GMM(data_set, init_centroids, init_cov, init_pi, k, tolerance, r=None):
    """Runs GMM using k clusters for r iterations (or until log likelyhood doesn't change)
    Returns gamma, log likelyhood, and the parameters"""
    # Run at least 1 iteration of GMM
    gamma = e_step(data_set, init_centroids, init_cov, init_pi, k)
    centroids, cov, pi = m_step(data_set, gamma)
    log_likelyhood = calc_log_likelyhood(data_set, centroids, cov, pi)
    count = 1

    # Go until we've reached the max number of iterations, or we've converged (log-likelyhood isn't changing)
    log_likelyhood_old = float("-inf")
    while log_likelyhood > (log_likelyhood_old + tolerance):
        if count >= r:
            break
        gamma = e_step(data_set, centroids, cov, pi, k)
        centroids, cov, pi = m_step(data_set, gamma)
        log_likelyhood_old = log_likelyhood
        log_likelyhood = calc_log_likelyhood(data_set, centroids, cov, pi)
        count += 1
    return gamma, log_likelyhood, centroids, cov, pi


def get_best_GMM(data_set, num_runs, k, tolerance, r):
    """Runs GMM with k clusters r number of times. Returns the best clustering from those r runs, and the log likelyhood of the resulting clustering"""
    runs_centroids = []
    runs_clusters = []
    max_log_likelyhood = float("-inf")

    for run in range(num_runs):
        init_centroids, init_cov, init_pi = initialize_GMM(data_set, k)
        gamma, log_likelyhood, centroids, cov, pi = run_GMM(data_set, init_centroids, init_cov, init_pi, k, tolerance, r)
        # Keep track of the best run
        if log_likelyhood > max_log_likelyhood:
            best_gamma, best_centroids, best_cov, best_pi, max_log_likelyhood = gamma, centroids, cov, pi, log_likelyhood
    return best_gamma, best_centroids, best_cov, best_pi, max_log_likelyhood



def main():
    global k_values
    global max_iterations
    global tolerance
    global num_runs
    global file_name
    data_set = kMeans.get_data_set(file_name)

    # Run the GMM algorithms with different values of k
    max_GMM_likelyhood = float("-inf")
    for k in k_values:
        gamma, centroids, cov, pi, log_likelyhood = get_best_GMM(data_set, num_runs, k, tolerance, max_iterations)

        # Keep track of which value of k gives the highest likelyhood
        if log_likelyhood > max_GMM_likelyhood:
            best_gamma = gamma
            max_GMM_likelyhood = log_likelyhood

        print("k = " + str(k))
        print("\tlog likelyhood = " + str(log_likelyhood))
        for cluster_index in range(len(centroids)):
            print("\tcluster " + str(cluster_index))
            print("\t\tcentroid =  " + str(centroids[cluster_index]))
            print("\t\tcov =  " + str(cov[cluster_index]))
            print("\t\tpi =  " + str(pi[cluster_index]))
        print("\t")



    classify(data_set, best_gamma) # Classify the points based on their gamma functions



if __name__ == "__main__":
    main()