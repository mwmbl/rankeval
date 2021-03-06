import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'
QUERIES_DATASET_PATH = DATA_DIR / 'queries.csv'
RANKINGS_DATASET_TEST_PATH = DATA_DIR / 'rankings-test.csv'


URLS_PATH = Path(os.environ['HOME']) / 'data' / 'tinysearch' / 'urls.sqlite3'
