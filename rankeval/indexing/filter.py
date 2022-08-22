"""
Filter the crawl data to data contained in the ranking evaluation train dataset.
"""
import glob
import gzip
import json
import os

from rankeval.paths import TRAIN_TERMS_PATH

CRAWL_DATA_PATH = f'{os.environ["HOME"]}/data/mwmbl/file'


def get_paths():
    for dirpath, dirs, files in os.walk(CRAWL_DATA_PATH):
        for filename in files:
            yield os.path.join(dirpath, filename)


def run():
    terms = set(json.load(open(TRAIN_TERMS_PATH)))

    for path in get_paths():
        data = json.load(gzip.GzipFile(path))
        print("Data", data)
        for item in data['items']:
            content = item['content']
            if content:
                text = ' '.join([content['title'], content['extract'], item['url']])
                print("Text", text)
                cleaned = text.lower().replace('.', ' ').replace('/', ' ').replace(',', ' ').replace(':', ' ')
                tokens = set(cleaned.split())
                if tokens & terms:
                    print("Tokens", tokens & terms)

        break



if __name__ == '__main__':
    run()
