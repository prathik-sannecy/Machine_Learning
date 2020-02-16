import unittest
from Programming_Assignment1.Source.kMeans import *


class test_kMeans(unittest.TestCase):
    def test_get_distance(self):
        point1 = [-1, -3]
        point2 = [3, 0]
        assert(get_distance(point1, point2) == 5)

    def test_calc_average_cluster(self):
        points = [[-1, -3], [3, 0], [4, 7]]
        assert(calc_average_cluster(points) == [2, float(4/3)])

    def test_classify_point(self):
        averages = [[-1, -3], [3, 0], [4, 7]]
        assert(classify_point([2, -1], averages) == 1)
        assert(classify_point([-7, -20], averages) == 0)

    def test_get_new_averages(self):
        clusters = [
            [[-3, -4], [-1000, -9000]],
            [[2, 1], [3, -1]],
            [[9, 100], [4, 8]]
        ]
        assert(get_new_averages(clusters)[0] == [-501.5, -4502])
        assert(get_new_averages(clusters)[1] == [2.5, 0])
        assert(get_new_averages(clusters)[2] == [6.5, 54])

    def test_create_new_clusters(self):
        averages = [[-1, -3], [3, 0], [4, 7]]
        data_set = [
            [-3, -4],
            [4, 8],
            [9, 100],
            [2, 1],
            [3, -1],
            [-1000, -9000]
        ]
        clusters = create_new_clusters(data_set, averages)
        assert(data_set[0] in clusters[0])
        assert(data_set[1] in clusters[2])
        assert(data_set[2] in clusters[2])
        assert(data_set[3] in clusters[1])
        assert(data_set[4] in clusters[1])
        assert(data_set[5] in clusters[0])





if __name__ == '__main__':
    unittest.main()
