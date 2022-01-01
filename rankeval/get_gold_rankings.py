"""
Retrieve the "gold standard" rankings from Bing Web Search.
"""

import os

import requests

BING_API_SUBSCRIPTION_KEY = os.environ['BING_API_SUBSCRIPTION_KEY']
BING_SEARCH_API_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"
BING_SUGGEST_API_ENDPOINT = "https://api.bing.microsoft.com/v7.0/Suggestions"


def retrieve_rankings(query):
    headers = {"Ocp-Apim-Subscription-Key": BING_API_SUBSCRIPTION_KEY}
    params = {"q": 'afghanistan', "mkt": "en-US", "textDecorations": False, "textFormat": "HTML"}
    response = requests.get(BING_SUGGEST_API_ENDPOINT, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    print("Web data", search_results)


if __name__ == '__main__':
    retrieve_rankings('afghanistan')
