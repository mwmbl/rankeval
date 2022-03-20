"""
Evaluate a learning to rank dataset.
"""
from argparse import ArgumentParser

import numpy as np
import pandas as pd
from scipy.stats import sem
from sklearn.base import BaseEstimator, clone
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.metrics import make_scorer, ndcg_score
from sklearn.model_selection import GroupKFold, cross_val_score

from rankeval.evaluation.evaluate import CLICK_PROPORTIONS
from rankeval.ltr.baseline import RandomRegressor
from rankeval.paths import LEARNING_TO_RANK_DATASET_PATH


PREDICTORS = {
    'random': RandomRegressor(),
    'constant': DummyRegressor(),
}


def get_discount(rank: float):
    if np.isnan(rank):
        return 0.0
    if rank >= len(CLICK_PROPORTIONS):
        return CLICK_PROPORTIONS[-1]
    return CLICK_PROPORTIONS[int(rank)]


def run():
    parser = ArgumentParser()
    parser.add_argument('--predictor', required=True, choices=sorted(PREDICTORS))

    args = parser.parse_args()

    predictor = PREDICTORS[args.predictor]

    dataset = pd.read_csv(LEARNING_TO_RANK_DATASET_PATH)
    dataset['gold_discount'] = dataset['gold_standard_rank'].apply(get_discount)

    print("Gold standard", dataset['gold_discount'])

    X = dataset[['query', 'url', 'title', 'extract', 'score']]
    y = dataset['gold_discount']
    groups = dataset['query']

    cross_validator = GroupKFold(n_splits=3)

    splits = cross_validator.split(X, y, groups)

    scores = []
    for train, test in splits:
        model = clone(predictor)
        model.fit(X.iloc[train], y.iloc[train])

        predictions = model.predict(X.iloc[test])

        test_dataset = dataset.iloc[test].copy()
        test_dataset['prediction'] = predictions
        for query, rankings in test_dataset.groupby('query'):
            if len(rankings) == 1:
                continue

            rankings_gold_discount = rankings['gold_discount'].tolist()
            rankings_prediction = rankings['prediction'].tolist()
            print("Rankings gold discount", rankings_gold_discount)
            print("Rankings prediction", rankings_prediction)
            score = ndcg_score([rankings_gold_discount], [rankings_prediction])
            scores.append(score)

    print("scores:", scores)
    print("mean_score:", np.mean(scores))
    print("stderr_score:", sem(scores))


if __name__ == '__main__':
    run()
