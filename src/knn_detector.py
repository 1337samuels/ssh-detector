
from detector import Detector
from utils import *
from consts import *

from logging import getLogger; logger = getLogger(LOGGER_NAME)


class KnnDetector(Detector):
    def __init__(self, training_set, testing_set):
        super(KnnDetector, self).__init__(training_set, testing_set)

    def test_detector(self, extra_parameter):
        assert extra_parameter % 2 == 1, "k has to be odd"
        correct = 0
        for sample in self.testing_set:
            logger.debug("Finding neighbors of sample {}".format(sample[ENTRY_ID_INDEX]))
            neighbors = self._get_neighbors(sample, extra_parameter)
            label_hist = {0:0, 1:0}
            for n in neighbors:
                label_hist[n[ENTRY_LABEL_INDEX]] += 1
            label = 0 if label_hist[0] > label_hist[1] else 1

            if label == sample[ENTRY_LABEL_INDEX]:
                correct += 1
        logger.debug("Got {} correct samples".format(correct))

        accuracy = correct / len(self.testing_set)
        logger.info("Accuracy: {}%".format(accuracy*100))
        return accuracy

    def _get_neighbors(self, new_instance, k):
        closest_neighbors = []
        for sample in self.training_set:
            d = eucledian_distance(sample[2:], new_instance[2:])
            if len(closest_neighbors) < k:
                closest_neighbors.append((sample, d))
            else:
                for n in closest_neighbors:
                    if n[1] > d:
                        closest_neighbors.remove(n)
                        closest_neighbors.append((sample, d))
                        break
        
        return [n[0] for n in closest_neighbors]
