
from consts import *
from db_reader import SqlDatabase
from utils import setup_logging, normalize_values
from knn_detector import KnnDetector
from tester import Tester

from logging import getLogger; logger = getLogger(LOGGER_NAME)

def perform_tests_on_db(db):
    t = Tester(db)

    features1 = ["duration", "dp_9_bytes", "dp_10_bytes", "dp_11_bytes", "dp_12_bytes"]
    logger.info("Testing features 1")
    t.update_samples_by_features(features1, 10000)

    logger.info("Testing KNN Detector on k=5")
    t.test_algorithm(KnnDetector, 5)



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
