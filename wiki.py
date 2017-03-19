"""
Wikipedia API

All requests to API go through https://en.wikipedia.org/w/api.php

Documentation on the query action is available at
* https://en.wikipedia.org/w/api.php?action=help&modules=query

"""
import sys
import re
import json
import requests

WIKI_API = 'https://en.wikipedia.org/w/api.php'
#WIKI_API = 'http://www.ganfyd.org/api.php'

# -----------------------------------------------------------------------------
# Lower level functions

def query_page_categories(titles, clcontinue=None):
    """
    Given a list of page titles, separated by '|', issue query to Wikipedia API
    to get the page categories.

    For details, refer to this page
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
    if clcontinue:
        params['clcontinue'] = clcontinue
    r = requests.get(WIKI_API, params=params)
    if r.status_code != 200:
        raise RuntimeError('Failed to retrieve page with params: {0}'.format(json.dumps(params)))
    return r.json()

def query_subcat(cat, cmcontinue=None):
    """
    Given a category, issue query to Wikipedia API to retrieve its subcategories.

    For details, refer to this page
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
    if cmcontinue:
        params['cmcontinue'] = cmcontinue
    r = requests.get(WIKI_API, params=params)
    if r.status_code != 200:
        raise RuntimeError('Failed to retrieve page with params: {0}'.format(json.dumps(params)))
    return r.json()

# -----------------------------------------------------------------------------
# Higher level functions

def get_page_categories(title):
    """
    Given a wikipedia page title, get list of categories associated with it.
    """
    categories = []
    r = query_page_categories(title)
    for _counter in range(100): # limit pagination to 100 queries
        pages = r['query']['pages']
        for (page_id, page) in pages.items():
            for c in page.get('categories', []):
                cat = c['title']
                if cat.startswith('Category:'):
                    cat = cat[len('Category:'):]
                categories.append(cat)
        if 'continue' not in r:
            break
        clcontinue = r['continue']['clcontinue']
        sys.stderr.write('{0}\n'.format(clcontinue))
        r = query_page_categories(title, clcontinue=clcontinue)
    return categories

def get_subcategories(cat):
    """
    Given a category, get its entire list of immediate subcategories.
    """
    subcats = []
    r = query_subcat(cat)
    for _counter in range(100): # limit pagination to 100 queries
        categorymembers = r['query']['categorymembers']
        for c in categorymembers:
            subcat = c['title']
            if subcat.startswith('Category:'):
                subcat = subcat[len('Category:'):]
            subcats.append(subcat)
        if 'continue' not in r:
            break
        cmcontinue = r['continue']['cmcontinue']
        sys.stderr.write('{0}\n'.format(cmcontinue))
        r = query_subcat(cat, cmcontinue=cmcontinue)
    return subcats

