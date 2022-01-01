"""
Retrieve the "gold standard" rankings from Bing Web Search.
"""

import os

import pandas as pd
from pandas import DataFrame

from rankeval.paths import QUERIES_DATASET_PATH, RANKINGS_DATASET_PATH
from rankeval.search_api import retrieve_rankings

BING_API_SUBSCRIPTION_KEY = os.environ['BING_API_SUBSCRIPTION_KEY']
BING_SEARCH_API_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"
BING_SUGGEST_API_ENDPOINT = "https://api.bing.microsoft.com/v7.0/Suggestions"


NUM_QUERIES = 100


def get_query_rankings() -> DataFrame:
    query_dataset = pd.read_csv(QUERIES_DATASET_PATH)

    # Get one suggestion for each query
    # Use this method: https://stackoverflow.com/a/46660098
    # Shuffle, then take the top item from each group
    queries = query_dataset.sample(frac=1.0)\
        .groupby('query')\
        .head()['suggestion']\
        .to_list()[:NUM_QUERIES]

    print("Queries", queries)

    dataset = []
    for query in queries:
        rankings = retrieve_rankings(query)
        print("Rankings", rankings)
        rankings_df = DataFrame(rankings)
        rankings_df['query'] = query
        dataset.append(rankings_df)
    return pd.concat(dataset)


def run():
    rankings = get_query_rankings()
    rankings.to_csv(RANKINGS_DATASET_PATH)


if __name__ == '__main__':
    run()
