
from consts import *
from db_reader import SqlDatabase
from utils import setup_logging
from detectors import KnnDetector, SvmDetector
from tester import Tester

from logging import getLogger; logger = getLogger(LOGGER_NAME)


def perform_tests_on_db(db, features, size):
    t = Tester(db)
    logger.info(f"Testing features {features}")
    t.update_samples_by_features(features, size)

    for k in KNN_VALUES:
        logger.info(f"Testing KNN Detector on k={k}")
        t.test_algorithm(KnnDetector, k)

    for k in SVM_KERNELS:
        logger.info(f"Testing SVM Detector on kernel={k}")
        t.test_algorithm(SvmDetector, k)


def feature_select(db : SqlDatabase, classifier):
    """
    Selects features from the DB based on the classifier using linear SVM detector
    :param db: SqlDatabase used for SQL queries
    :param classifier: name of labels
    :return: List of features sorted by their weight
    """
    features = db.get_column_names()
    assert classifier in features, "Classifier must be in features"
    features = db.execute(f"select name from pragma_table_info('{FLOW_TABLE}') where type='integer';")
    features = [f[0] for f in features if f[0] not in ['id', classifier]]
    logger.debug(f"All possible integer features are: {features}")

    t = Tester(db)
    t.update_samples_by_features(features, None)
    outfeatures = t.find_features(SvmDetector, "linear")
    features = list(zip(features, outfeatures[0]))
    features.sort(key=lambda x: abs(x[1]), reverse=True)
    logger.info(f"Features ordered by weights: {features}")
    return [f[0] for f in features]


def main_logic(db):
    logger.info("Selecting Features")
    our_features = feature_select(db, "bruteforce")[:len(PAPER_FEATURES)]
    logger.debug(f"Chose features {our_features}")

    logger.info("Running tests on features from paper!")
    perform_tests_on_db(db, PAPER_FEATURES, 15000)

    logger.info("Running tests on features we chose by SVM weight!")
    perform_tests_on_db(db, our_features, 15000)


def main():
    setup_logging()
    logger.critical("Welcome to the SSH Detector!")
    db = SqlDatabase(DB_PATH, default_table=FLOW_TABLE)
    db.open()
    logger.debug("Opened DB")
    try:
        main_logic(db)
    finally:
        db.close()
        logger.debug("Closed DB")
    logger.critical("SSH Detector finished successfully :)")
    return 0


if __name__ == '__main__':
    main()
