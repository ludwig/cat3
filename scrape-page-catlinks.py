#!/usr/bin/env python3

import os, sys
import requests
import re
import json

from urllib.parse import urlparse
from bs4 import BeautifulSoup

def wiki_categories(url):
    r = requests.get(url)
    if r.status_code != 200:
        sys.stderr.write("Could not fetch {0}\n".format(url))
        sys.exit(1)
    html_doc = r.text

    soup = BeautifulSoup(html_doc, 'html.parser')
    #catlinks = soup.find(id='catlinks')
    catlinks = soup.find(id='mw-normal-catlinks')

    categories = []
    for a in catlinks.find_all('a'):
        catlink = a.attrs['href']
        m = re.match(r'/wiki/Category:(?P<category>.*)', catlink)
        if m:
            categories.append(m.group('category'))

    return categories


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("{0} URL\n".format(sys.argv[0]))
        sys.exit(1)

    url = sys.argv[1]
    sys.stderr.write("Fetching {0}\n".format(url))

    categories = wiki_categories(url)
    print(json.dumps(categories, indent=2))


if __name__ == "__main__":
    main()
