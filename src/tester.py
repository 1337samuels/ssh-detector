import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from consts import *
from utils import normalize_values
from logging import getLogger; logger = getLogger(LOGGER_NAME)

class Tester(object):
    def __init__(self, db):
        self.db = db
        self.samples = None

    def update_samples_by_features(self, feature_list, size):
        features = ','.join([f"`{f}`" for f in feature_list])
        # duration, dp_9_bytes, dp_10_bytes, dp_11_bytes, dp_12_bytes
        logger.debug("Reading features from DB")
        samples = self.db.execute("select bruteforce,{features} from {table};".format(features=features, table=FLOW_TABLE))

        size = size if size else len(samples)
        samples = random.sample(samples, size)
        assert len(samples) == size, "Sample size isn't equal to amount wanted"

        logger.debug("Normalizing sampled values")
        norm_samples = normalize_values(samples)
        self.labels = [s[0] for s in norm_samples]
        self.data = [s[1:] for s in norm_samples]

    def test_algorithm(self, detector, extra_param=None):
        sep_param = 0.5
        data_train, data_test, labels_train, labels_test = train_test_split(
            self.data, self.labels, test_size=sep_param)

        d = detector(data_train, data_test, labels_train, extra_param)
        predictions = d.test_detector()
        logger.debug("Results:")
        logger.debug("\n{}".format(confusion_matrix(labels_test, predictions)))
        logger.debug("\n{}".format(classification_report(labels_test, predictions)))

    def find_features(self, detector, extra_parameter):
        d = detector(self.data, [], self.labels, extra_parameter)
        return d.extract_features()

        