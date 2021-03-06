from sklearn.svm import SVC

from detectors.base_detector import Detector
from utils import *
from consts import *

from logging import getLogger; logger = getLogger(LOGGER_NAME)


class SvmDetector(Detector):
    def __init__(self, data_train, data_test, labels_train, extra_parameter):
        super(SvmDetector, self).__init__(data_train, data_test, labels_train, extra_parameter)

    def test_detector(self, ):
        svclassifier = SVC(kernel=self.extra_parameter)
        svclassifier.fit(self.data_train, self.labels_train)
        if self.extra_parameter == "linear":
            logger.debug(f"Weights are: {svclassifier.coef_}")
        return svclassifier.predict(self.data_test)

    def extract_features(self):
        svclassifier = SVC(kernel="linear")
        svclassifier.fit(self.data_train, self.labels_train)
        return svclassifier.coef_

