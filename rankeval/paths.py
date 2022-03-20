import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'
QUERIES_DATASET_PATH = DATA_DIR / 'queries.csv'

REMOTE_DATA_DIR = Path(__file__).parent.parent / 'remote-datasets'
RANKINGS_DATASET_TRAIN_PATH = REMOTE_DATA_DIR / 'rankings-train.csv'
RANKINGS_DATASET_TEST_PATH = REMOTE_DATA_DIR / 'rankings-test.csv'


LEARNING_TO_RANK_DATASET_PATH = DATA_DIR / 'learning-to-rank.csv'

URLS_PATH = Path(os.environ['HOME']) / 'data' / 'tinysearch' / 'urls.sqlite3'
