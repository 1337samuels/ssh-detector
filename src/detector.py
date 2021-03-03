from abc import abstractmethod


class Detector(object):
    def __init__(self, training_set, testing_set):
        self.training_set = training_set
        self.testing_set = testing_set

    @abstractmethod
    def test_detector(self, extra_parameter):
        raise NotImplementedError("Not implemented test_detector method for abstract detector")