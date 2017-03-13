#!/usr/bin/env python3

import sys
import json
import requests

WIKI_API = 'https://en.wikipedia.org/w/api.php'
#WIKI_API = 'https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtype=subcat&cmtitle=Category:Anatomy'

CATEGORIES = set()

def wiki_query_subcat(cat, **kwargs):
    """
    For API details, refer to this page
    * https://en.wikipedia.org/w/api.php?action=help&modules=query+categorymembers
    """
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'categorymembers',
        'cmtype': 'subcat',
        'cmlimit': '500', # max cmlimit for unregistered robots is 500
        'cmtitle': 'Category:{0}'.format(cat),
    }
    cmcontinue = kwargs.get('cmcontinue')
    if cmcontinue:
        params['cmcontinue'] = cmcontinue

    r = requests.get(WIKI_API, params=params)
    if r.status_code != 200:
        raise RuntimeError('Failed to retrieve page with params: {0}'.format(json.dumps(params)))
    return r.json()

def fetch_subcategories(cat):
    subcats = []
    r = wiki_query_subcat(cat)
    for _counter in range(100): # limit pagination to 100 queries
        categorymembers = r['query']['categorymembers']
        for c in categorymembers:
            subcat = c['title'][len('Category:'):]
            subcats.append(subcat)
        if 'continue' not in r:
            break
        cmcontinue = r['continue']['cmcontinue']
        sys.stderr.write('{0}\n'.format(cmcontinue))
        r = wiki_query_subcat(cat, cmcontinue=cmcontinue)
    return subcats


def main():
    if len(sys.argv) < 2:
        # NOTE: The category can be specified with either spaces or underscores.
        sys.stderr.write("{0} CATEGORY\n".format(sys.argv[0]))
        sys.exit(1)

    category = sys.argv[1]

    #obj = wiki_query_subcat(category)
    obj = fetch_subcategories(category)

    json.dump(obj, sys.stdout, indent=2)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()
