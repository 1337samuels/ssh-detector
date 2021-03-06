
from consts import *
from db_reader import SqlDatabase
from utils import setup_logging
from detectors import KnnDetector, SvmDetector
from tester import Tester
from sklearn.model_selection import train_test_split

from logging import getLogger; logger = getLogger(LOGGER_NAME)

def perform_tests_on_db(db):
    t = Tester(db)

    features1 = ["duration", "dp_9_bytes", "dp_10_bytes", "dp_11_bytes", "dp_12_bytes"]
    features2 = ["bytes_out", "avgp_len", "num_pkts_out", "varp_len"]
    fs = [features1, features2]

    for i in range(len(fs)):
        logger.info("Testing features {}".format(i))
        t.update_samples_by_features(fs[i], 500)

        ks = [3, 5, 7]
        for k in ks:
            logger.info("Testing KNN Detector on k={}".format(k))
            t.test_algorithm(KnnDetector, k)

        svm_kernels = ['linear', 'poly', 'rbf']
        for k in svm_kernels:
            logger.info("Testing SVM Detector on kernel={}".format(k))
            t.test_algorithm(SvmDetector, k)

def feature_select(db : SqlDatabase, classifier):
    features = db.get_column_names()
    assert classifier in features, "Classifier must be in features"
    features = db.execute(f"select name from pragma_table_info('{FLOW_TABLE}') where type='integer';")
    features = [f[0] for f in features if f[0] not in ['id', 'bruteforce']]
    logger.info(f"Features are: {features}")
    t = Tester(db)
    t.update_samples_by_features(features, 70000)
    outfeatures = t.find_features(SvmDetector)
    features = list(zip(features, outfeatures[0]))
    features.sort(key=lambda x: abs(x[1]), reverse=True)
    logger.info(f"Features ordered by weights: {features}")

def main():
    setup_logging()
    logger.critical("Welcome to the SSH Detector!")
    db = SqlDatabase(DB_PATH, default_table=FLOW_TABLE)
    db.open()
    logger.debug("Opened DB")
    try:
        logger.debug("Start tests")
        feature_select(db, "bruteforce")
    finally:
        db.close()
        logger.debug("Closed DB")
    logger.critical("Code finished successfully :)")
    return 0


if __name__ == '__main__':
    main()
