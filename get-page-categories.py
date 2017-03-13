#!/usr/bin/env python3

import sys
import re
import json
import requests
from urllib.parse import urlparse

WIKI_API = 'https://en.wikipedia.org/w/api.php'
# Refer to https://en.wikipedia.org/w/api.php?action=help&modules=query to see what you can query

def wiki_query_categories(titles, **kwargs):
    """
    For API details, refer to this page
    * https://en.wikipedia.org/w/api.php?action=help&modules=query+categories
    """
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'categories',
        'clshow': '!hidden',
        'cllimit': '500', # max cllimit for unregistered robots is 500
        'titles': titles,
    }
    clcontinue = kwargs.get('clcontinue')
    if clcontinue:
        params['clcontinue'] = clcontinue
    r = requests.get(WIKI_API, params=params)
    if r.status_code != 200:
        raise RuntimeError('Failed to retrieve page with params: {0}'.format(json.dumps(params)))
    return r.json()

def get_page_title(url):
    parsed_url = urlparse(url)
    m = re.match(r'/wiki/(?P<title>.*)', parsed_url.path)
    return m.group('title')

def get_page_categories(title):
    categories = []
    r = wiki_query_categories(title)
    for _counter in range(100): # limit pagination to 100 queries
        pages = r['query']['pages']
        for (page_id, page) in pages.items():
            for c in page.get('categories', []):
                cat = c['title'][len('Category:'):]
                categories.append(cat)
        if 'continue' not in r:
            break
        clcontinue = r['continue']['clcontinue']
        sys.stderr.write('{0}\n'.format(clcontinue))
        r = wiki_query_categories(title, clcontinue=clcontinue)
    return categories

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("{0} URL\n".format(sys.argv[0]))
        sys.exit(1)

    url = sys.argv[1]
    title = get_page_title(url)

    #obj = wiki_query_categories(title)
    obj = get_page_categories(title)

    json.dump(obj, sys.stdout, indent=2)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()
