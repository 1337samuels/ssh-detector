from abc import abstractmethod


class Detector(object):
    def __init__(self, data_train, data_test, labels_train, extra_parameter):
        assert len(data_train) == len(labels_train), "Mismatch size"
        self.data_train = data_train
        self.data_test = data_test
        self.labels_train = labels_train
        self.extra_parameter = extra_parameter

    @abstractmethod
    def test_detector(self):
        raise NotImplementedError("Not implemented test_detector method for detector")

    @abstractmethod
    def extract_features(self):
        raise NotImplementedError("Not implemented extract_features method for detector")