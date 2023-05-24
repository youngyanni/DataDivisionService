from os import path
import sys

sys.path.append(path.abspath('../src'))
from src.request_handlers import *

request = {
    "modelLabel": "SPLIT",
    "dataset": [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]],
    "type": "k-fold",
    "properties": {
        "n_splits": 2,
        "part": 4,
        "test_size": 0.6,
        "shuffle": True,
        "random_state": 2,
    },
    "train_test": []
}

split_data(request)
