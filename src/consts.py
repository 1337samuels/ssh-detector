# Project consts
DB_PATH = '../DB/ssh-annotated.sqlite'
LOG_PATH = '../logs/ssh_detector_{}_{}_{}_{}_{}_{}.log'
LOGGER_NAME = 'ssh_detector_logger'

# DB consts
URI_STRING = 'file:{path}?mode=ro'
ENTRY_ID_INDEX = 0
ENTRY_LABEL_INDEX = 1
FLOW_TABLE = 'flows'
PAPER_FEATURES = ["duration", "num_pkts_in", "num_pkts_out", "bytes_in", "bytes_out", "avg_ipt", "med_ipt", "dp_9_bytes", "dp_10_bytes", "dp_11_bytes", "dp_12_bytes"]

# ML consts
KNN_VALUES = [3, 5, 7]
SVM_KERNELS = ['linear', 'poly', 'rbf']
TRAIN_TEST_PARTITION = 0.5