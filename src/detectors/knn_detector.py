from detectors.base_detector import Detector
from utils import *
from consts import *

from logging import getLogger; logger = getLogger(LOGGER_NAME)


class KnnDetector(Detector):
    def __init__(self, data_train, data_test, labels_train, extra_parameter):
        assert extra_parameter % 2 == 1, "k has to be odd"
        super(KnnDetector, self).__init__(data_train, data_test, labels_train, extra_parameter)

    def test_detector(self):
        predictions = []
        for i in range(len(self.data_test)):
            neighbor_labels = self._get_neighbor_labels(self.data_test[i])
            predictions.append(get_majority(neighbor_labels))

        return predictions

    def _get_neighbor_labels(self, testing_sample):
        # closest_neighbors is a list of tuples, where every tuple is (index of a sample, distance to testing_sample)
        closest_neighbors = []
        for i in range(len(self.data_train)):
            d = eucledian_distance(self.data_train[i], testing_sample)
            if len(closest_neighbors) < self.extra_parameter:
                closest_neighbors.append((i, d))
            else:
                for n in closest_neighbors:
                    if n[1] > d:
                        closest_neighbors.remove(n)
                        closest_neighbors.append((i, d))
                        break
        assert len(closest_neighbors) == self.extra_parameter, "Closest neighbors aren't k sized!"
        return [self.labels_train[n[0]] for n in closest_neighbors]
