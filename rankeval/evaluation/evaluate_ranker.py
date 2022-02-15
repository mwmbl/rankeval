import os
import sys

from mwmbl.tinysearchengine.app import get_config_and_index
from mwmbl.tinysearchengine.indexer import TinyIndex, Document, NUM_PAGES, PAGE_SIZE
from mwmbl.tinysearchengine.rank import Ranker

from rankeval.evaluation.evaluate import RankingModel, evaluate


class MwmblRankingModel(RankingModel):
    def __init__(self, ranker: Ranker):
        self.ranker = ranker

    def predict(self, query: str) -> list[str]:
        results = self.ranker.search(query)
        return [x['url'] for x in results]


class DummyCompleter:
    def complete(self, q):
        return [q]


def run():
    index_path = sys.argv[1]

    completer = DummyCompleter()

    tiny_index = TinyIndex(
        item_factory=Document,
        index_path=index_path,
        num_pages=NUM_PAGES,
        page_size=PAGE_SIZE,
    )

    ranker = Ranker(tiny_index, completer)
    model = MwmblRankingModel(ranker)
    evaluate(model)


if __name__ == '__main__':
    run()
