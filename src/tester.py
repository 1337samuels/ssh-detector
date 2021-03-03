import random

from consts import *
from utils import normalize_values
from logging import getLogger; logger = getLogger(LOGGER_NAME)

class Tester(object):
    def __init__(self, db):
        self.db = db
        self.samples = None

    def update_samples_by_features(self, feature_list, size):
        features = ','.join(feature_list)
        # duration, dp_9_bytes, dp_10_bytes, dp_11_bytes, dp_12_bytes
        logger.debug("Reading features from DB")
        samples = self.db.execute("select id,bruteforce,{features} from {table};".format(features=features, table=FLOW_TABLE))

        samples = random.sample(samples, size)
        assert len(samples) == size, "Sample size isn't equal to amount wanted"

        logger.info("Normalizing sampled values")
        self.samples = normalize_values(samples)

    def test_algorithm(self, detector, extra_param=None):
        #TODO: Cross validation
        sep_param = 0.5
        train = self.samples[:round(len(self.samples)*sep_param)]
        test = self.samples[round(len(self.samples)*sep_param):]
        d = detector(train, test)
        d.test_detector(extra_param)

