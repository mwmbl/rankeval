"""
Create a dataset of plausible queries using autosuggest.
"""
from random import Random

from pandas import DataFrame

from rankeval.paths import QUERIES_DATASET_PATH
from rankeval.dataset.search_api import retrieve_suggestions

SEED_TERMS = {'ebay'}

DATASET_SIZE = 1000

random = Random(1)


def full_term(term: str) -> str:
    return term


def first_two_characters(term: str) -> str:
    return term[:2]


def create_dataset() -> list[dict[str, str]]:
    dataset = []
    done_queries = set()
    terms = set(SEED_TERMS)

    while len(dataset) < DATASET_SIZE:
        term = random.choice(list(terms))
        query_type = random.choice([full_term, first_two_characters])
        query = query_type(term)

        if query in done_queries:
            continue

        suggestions = retrieve_suggestions(query)
        dataset += [{'query': query, 'suggestion': suggestion} for suggestion in suggestions]
        done_queries.add(query)
        for suggestion in suggestions:
            terms |= set(suggestion.split())
        print(f'Query: {query}, suggestions: {suggestions}')

    return dataset


def save_dataset(dataset: list[dict[str, str]]):
    DataFrame(dataset).to_csv(QUERIES_DATASET_PATH)


def run():
    dataset = create_dataset()
    save_dataset(dataset)


if __name__ == '__main__':
    run()
