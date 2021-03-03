from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import LabelEncoder
from db_reader import SqlDatabase
import pandas as pd
from consts import *
from logging import getLogger; logger = getLogger(LOGGER_NAME)

columns = [
    ('idp_in', False),
    ('idp_out', False),
    ('dp', True),
    ('sp', True),
    ('entropy', False),
    ('total_entropy', False),
    ('duration', False),
    ('pr', False),
    ('fdp_len', False),
    ('ldp_len', False),
    ('num_pkts_in', False),
    ('num_pkts_out', False),
    ('num_pkts', False),
    ('bytes_in', False),
    ('bytes_out', False),
    ('avg_ipt', False),
    ('med_ipt', False),
    ('var_ipt', False),
    ('ssh_client', True),
    ('avgp_len', False),
    ('varp_len', False),
    ('ssh_version', True),
    ('medp_len', False),
    ('kex_algos_lenght', False),
    ('encryption_algo_lenght', False),
    ('first_encryption_algo', True),
    ('3des-cbc', True),
    ('3des-ctr', True),
    ('aes128-cbc', True),
    ('aes128-ctr', True),
    ('aes128-gcm@openssh.com', True),
    ('aes192-cbc', True),
    ('aes192-ctr', True),
    ('aes256-cbc', True),
    ('aes256-ctr', True),
    ('aes256-gcm@openssh.com', True),
    ('arcfour', True),
    ('arcfour128', True),
    ('arcfour256', True),
    ('blowfish-cbc', True),
    ('blowfish-ctr', True),
    ('cast128-cbc', True),
    ('chacha20-poly1305@openssh.com', True),
    ('des-cbc-ssh1', True),
    ('rijndael-cbc@lysator.liu.se', True),
    ('twofish128-cbc', True),
    ('twofish256-cbc', True),
    ('support_other_enc', True),
    ('interflow_gap', False),
    ('fp_bytes', False),
    ('dp_6_bytes', False),
    ('dp_7_bytes', False),
    ('dp_8_bytes', False),
    ('dp_9_bytes', False),
    ('dp_10_bytes', False),
    ('dp_11_bytes', False),
    ('dp_12_bytes', False),
    ('dp_13_bytes', False),
    ('dp_15_bytes', False),
    ('dp_16_bytes', False),
    ('fin_count', False),
    ('reset_count', False)
]

class FeaturesExtractor():
    def __init__(self, database : SqlDatabase):
        self.db = database
    
    def get_features_information_gain(self, label):
        column_names = self.db.get_column_names()
        information_gains = []
        assert label in column_names, f'{label} is not a column'
        classifications = pd.DataFrame([c[0] for c in self.db.execute(f"select `{label}` FROM {FLOW_TABLE};")])
        features = ','.join([f'`{c}`' for c in [c1[0] for c1 in columns] if c != label])
        features_data = pd.DataFrame(self.db.execute(f"select {features} from {FLOW_TABLE};"))
        for (column, i) in zip(columns, range(len(columns))):
            if column[1]:
                logger.info(f"Labeling {column}")
                le = LabelEncoder()
                le.fit(features_data[i])
                features_data[i] = le.transform(features_data[i])
        #     values = [c[0] for c in self.db.execute(f"select `{column}` from {FLOW_TABLE};")]
        #     if type(values[0]) == str:
        #         values = [c if c != None else "" for c in values]
        #     information_gains.append((column, mutual_info_classif(classifications, values)))
        # information_gains.sort(key=lambda x: x[1], reverse=True)

        mutual_info = mutual_info_classif(features_data, classifications, discrete_features=[c1[1] for c1 in columns])
        mutual_info = [(a[0], m) for a,m in zip(columns, mutual_info)]
        mutual_info.sort(key=lambda x: x[1], reverse=True)
        return mutual_info