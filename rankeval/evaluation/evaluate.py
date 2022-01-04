"""
Perform an evaluation using NDCG against a gold standard set of results.
"""
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
from scipy.stats import sem
from sklearn.metrics import ndcg_score

from rankeval.paths import RANKINGS_DATASET_PATH


# Sourced from https://www.searchenginejournal.com/google-first-page-clicks/374516/
CLICK_PROPORTIONS = [0.285, 0.157, 0.110, 0.080, 0.072, 0.051, 0.040, 0.032, 0.028, 0.025]
NUM_RESULTS_FOR_EVAL = len(CLICK_PROPORTIONS)


class RankingModel(ABC):
    @abstractmethod
    def predict(self, query: str) -> list[str]:
        """
        Generate a list of URLs as search results for the given query.
        """
        pass


def evaluate(ranking_model: RankingModel):
    dataset = pd.read_csv(RANKINGS_DATASET_PATH)
    ndcg_scores = []
    proportions = []
    for query, rankings in dataset.groupby('query'):
        top_ranked = rankings[['url']].iloc[:NUM_RESULTS_FOR_EVAL]
        top_ranked['score'] = CLICK_PROPORTIONS
        scores = top_ranked.set_index('url')['score'].to_dict()
        print("Query", query, scores)

        predicted_urls = ranking_model.predict(query)
        top_urls = predicted_urls[:NUM_RESULTS_FOR_EVAL]
        y_true = [scores.get(url, 0.0) for url in top_urls] + [0.0] * (10 - len(top_urls))
        y_predicted = list(range(NUM_RESULTS_FOR_EVAL, 0, -1))

        print("Y true", y_true)
        print("Y predicted", y_predicted)

        proportion_matched = len(set(top_urls) & scores.keys()) / NUM_RESULTS_FOR_EVAL
        proportions.append(proportion_matched)

        score = ndcg_score([y_true], [y_predicted])
        ndcg_scores.append(score)

    print("Mean NDCG score", np.mean(ndcg_scores))
    print("Std error", sem(ndcg_scores))
    print()
    print("Mean proportion score", np.mean(proportions))
    print("Std error", sem(proportions))
