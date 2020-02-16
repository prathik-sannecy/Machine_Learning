import Programming_Assignment1.Source.kMeans as kMeans
import numpy as np
from scipy.stats import norm, multivariate_normal

num_runs = 10 # number of runs to try clustering on. Chooses the best clustering based on which run had the least error
k_values = range(3, 6) # which k values to run kmeans on


def initialize_GMM(data_set_file, k):

    global num_runs
    data_set = kMeans.get_data_set(data_set_file)
    initial_centroids = kMeans.initialize_centroids(data_set, k)
    init_clusters, init_centroids = kMeans.run_kmeans(data_set, initial_centroids)
    init_cov = [np.cov([point[0] for point in cluster], [point[1] for point in cluster]).tolist() for cluster in init_clusters]
    init_pi = [len(cluster) / len(data_set) for cluster in init_clusters]
    assert(sum(init_pi) == 1)
    return data_set, initial_centroids, init_cov, init_pi

def e_step(data_set, centroids, init_cov, pi, k):
    # gamma is a num of clusters x num of datapoints size 2D matrix
    gamma = [[0]*len(data_set) for _ in range(k)]
    for cluster_data_set_index in range(k):
        for i in range(len(data_set)):
            var = multivariate_normal(centroids[cluster_data_set_index], init_cov[cluster_data_set_index])
            var_pdf = var.pdf(data_set[i])
            gamma[cluster_data_set_index][i] = pi[cluster_data_set_index] * var_pdf
    datapoint_normalization = []
    for i in range(len(data_set)):
        datapoint_normalization.append(sum([cluster[i] for cluster in gamma]))
    for cluster_data_set_index in range(k):
        for i in range(len(data_set)):
            gamma[cluster_data_set_index][i] /= datapoint_normalization[i]
    return gamma



def main():
    global k_values
    data_set, initial_centroids, init_cov, init_pi = initialize_GMM(r"../Input_Files/GMM_dataset 546.txt", k_values[0])
    e_step(data_set, initial_centroids, init_cov, init_pi, k_values[0])

if __name__ == "__main__":
    main()