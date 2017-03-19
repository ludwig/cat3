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

WIKI_API = {
    'wikipedia': 'https://en.wikipedia.org/w/api.php',
    'ganfyd': 'http://www.ganfyd.org/api.php',
}


class API(object):

    def __init__(self, site='wikipedia'):
        self.api = WIKI_API[site]

    def query_page_categories(self, titles, clcontinue=None):
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
        r = requests.get(self.api, params=params)
        if r.status_code != 200:
            raise RuntimeError('Failed to retrieve page with params: {0}'.format(json.dumps(params)))
        return r.json()

    def query_category_subcat(self, cat, cmcontinue=None):
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
        r = requests.get(self.api, params=params)
        if r.status_code != 200:
            raise RuntimeError('Failed to retrieve page with params: {0}'.format(json.dumps(params)))
        return r.json()

    def query_category_pages(self, cat, cmcontinue=None):
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'categorymembers',
            'cmtype': 'page',
            'cmlimit': '500', # max cmlimit for unregistered robots is 500
            'cmtitle': 'Category:{0}'.format(cat),
        }
        if cmcontinue:
            params['cmcontinue'] = cmcontinue
        r = requests.get(self.api, params=params)
        if r.status_code != 200:
            raise RuntimeError('Failed to retrieve page with params: {0}'.format(json.dumps(params)))
        return r.json()

    def get_page_categories(self, title):
        """
        Given a wikipedia page title, get list of categories associated with it.
        """
        categories = []
        r = self.query_page_categories(title)
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
            r = self.query_page_categories(title, clcontinue=clcontinue)
        return categories

    def get_category_subcategories(self, cat):
        """
        Given a category, get its entire list of immediate subcategories.
        """
        subcats = []
        r = self.query_category_subcat(cat)
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
            r = self.query_category_subcat(cat, cmcontinue=cmcontinue)
        return subcats

    def get_category_pages(self, cat):
        """
        Given a category, get its entire list of pages.
        """
        pages = []
        r = self.query_category_pages(cat)
        for _counter in range(500):
            categorymembers = r['query']['categorymembers']
            for p in categorymembers:
                page = p['title']
                pages.append(page)
            if 'continue' not in r:
                break
            cmcontinue = r['continue']['cmcontinue']
            sys.stderr.write('{0}\n'.format(cmcontinue))
            r = self.query_category_pages(cat, cmcontinue=cmcontinue)
        return pages


