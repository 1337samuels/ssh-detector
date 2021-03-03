
from consts import *
from db_reader import SqlDatabase
from utils import setup_logging
from detectors import KnnDetector, SvmDetector
from tester import Tester

from logging import getLogger; logger = getLogger(LOGGER_NAME)

def perform_tests_on_db(db):
    t = Tester(db)

    features1 = ["duration", "dp_9_bytes", "dp_10_bytes", "dp_11_bytes", "dp_12_bytes"]
    logger.info("Testing features 1")
    t.update_samples_by_features(features1, 2000)

    ks = [3, 5, 7]
    for k in ks:
        logger.info("Testing KNN Detector on k={}".format(k))
        t.test_algorithm(KnnDetector, k)

    svm_kernels = ['linear', 'poly', 'rbf']
    for k in svm_kernels:
        logger.info("Testing SVM Detector on kernel={}".format(k))
        t.test_algorithm(SvmDetector, k)

def main():
    setup_logging()
    logger.critical("Welcome to the SSH Detector!")
    db = SqlDatabase(DB_PATH, default_table=FLOW_TABLE)
    db.open()
    logger.debug("Opened DB")
    try:
        logger.debug("Start tests")
        perform_tests_on_db(db)
        #print(db.execute("select count(*) from {};".format(FLOW_TABLE))[0])
    finally:
        db.close()
        logger.debug("Closed DB")
    logger.critical("Code finished successfully :)")
    return 0


if __name__ == '__main__':
    main()
