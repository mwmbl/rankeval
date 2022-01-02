"""
Evaluate the crawled URLs to see how well they cover our gold-standard search results.
"""
import os
from pathlib import Path

from rankeval.evaluation.evaluate import evaluate, RankingModel


class OracleRankingModel(RankingModel):
    def predict(self, query: str) -> list[str]:
        return []


if __name__ == '__main__':
    evaluate(OracleRankingModel())
