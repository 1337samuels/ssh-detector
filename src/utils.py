import datetime
import logging
import math

from consts import *
from logging import getLogger; logger = getLogger(LOGGER_NAME)

def setup_logging():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('(%(asctime)s) %(levelname)s: %(message)s', datefmt='%H:%M:%S')

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    cur_time = datetime.datetime.now()
    fi = logging.FileHandler(LOG_PATH.format(cur_time.year, cur_time.month, cur_time.day, cur_time.hour,
                                             cur_time.minute, cur_time.second))
    fi.setLevel(logging.DEBUG)
    fi.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fi)


def eucledian_distance(vec1, vec2):
    assert len(vec1) == len(vec2), "Can't compare distances of different sized vectors"
    distance = 0
    for i in range(len(vec1)):
        distance += pow((float(vec1[i]) - float(vec2[i])), 2)
    return math.sqrt(distance)

def normalize_values(vecs):
    normalized_vectors = []
    min_values = list(map(min, zip(*vecs)))
    max_values = list(map(max, zip(*vecs)))

    for vec in vecs:
        new_vec = [vec[0], vec[1]]
        for value_index in range(2, len(vecs[0])):
            offset_value = vec[value_index] - min_values[value_index]
            offset_max = max_values[value_index] - min_values[value_index]
            normalized_value = offset_value / offset_max
            new_vec.append(normalized_value)
        normalized_vectors.append(new_vec)

    return normalized_vectors

def get_majority(values):
    label_hist = {0: 0, 1: 0}
    for l in values:
        label_hist[l] += 1
    return 0 if label_hist[0] > label_hist[1] else 1