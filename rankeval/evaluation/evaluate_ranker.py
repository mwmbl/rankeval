import pickle
import sys

from mwmbl.tinysearchengine.indexer import TinyIndex, Document
from mwmbl.tinysearchengine.ltr_rank import LTRRanker
from mwmbl.tinysearchengine.rank import Ranker

from rankeval.evaluation.evaluate import RankingModel, evaluate
from rankeval.paths import MODEL_PATH


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

    with TinyIndex(item_factory=Document, index_path=index_path) as tiny_index:
        # ranker = Ranker(tiny_index, completer)
        model = pickle.load(open(MODEL_PATH, 'rb'))
        ranker = LTRRanker(model, tiny_index, completer)
        model = MwmblRankingModel(ranker)
        evaluate(model)


if __name__ == '__main__':
    run()
