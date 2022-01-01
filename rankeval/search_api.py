"""
Wrapper for the Bing Search API to simplify usage.
"""
import os
from time import sleep

import requests

BING_API_SUBSCRIPTION_KEY = os.environ['BING_API_SUBSCRIPTION_KEY']
BING_SEARCH_API_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"
BING_SUGGEST_API_ENDPOINT = "https://api.bing.microsoft.com/v7.0/Suggestions"
SLEEP_TIME = 0.34


def retrieve_from_endpoint(query, endpoint, **args):
    headers = {"Ocp-Apim-Subscription-Key": BING_API_SUBSCRIPTION_KEY}
    params = {"q": query, "mkt": "en-US", "textDecorations": False, "textFormat": "HTML"}
    params.update(args)
    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    sleep(SLEEP_TIME)
    return search_results


def retrieve_suggestions(query):
    data = retrieve_from_endpoint(query, BING_SUGGEST_API_ENDPOINT)
    print("Got data", data)
    results = []
    for group in data['suggestionGroups']:
        results += [suggestion['displayText'] for suggestion in group['searchSuggestions']]
    return results


def retrieve_rankings(query):
    data = retrieve_from_endpoint(query, BING_SEARCH_API_ENDPOINT, count=50)
    return data['webPages']['value']
