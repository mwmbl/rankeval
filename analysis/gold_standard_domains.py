"""
Analyse gold standard domains to get an understanding for how many we need, and how many results
are typically root pages.
"""
from collections import Counter
from urllib.parse import urlparse

import pandas as pd

from rankeval.paths import RANKINGS_DATASET_PATH


def analyse_domains():
    gold_standard = pd.read_csv(RANKINGS_DATASET_PATH)
    urls = gold_standard['url']
    domains = urls.apply(lambda x: urlparse(x).hostname)
    domain_counts = Counter(domains)
    print("Top domains")
    for domain, count in domain_counts.most_common(100):
        print(domain, count)
    print("Total number of domains", len(domain_counts))
    print("Total number of URLs", len(urls))

    root_pages = urls.apply(lambda x: urlparse(x).path in {'/', ''}).sum()
    print("Number of root pages", root_pages)


if __name__ == '__main__':
    analyse_domains()
