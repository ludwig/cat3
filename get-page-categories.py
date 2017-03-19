#!/usr/bin/env python3

import sys
import re
import json
import wiki

from urllib.parse import urlparse

# Example: https://en.wikipedia.org/w/api.php?action=query&format=json&prop=categories&clshow=!hidden&cllimit=500&titles=Heart

def get_page_title(url):
    parsed_url = urlparse(url)
    m = re.match(r'/wiki/(?P<title>.*)', parsed_url.path)
    return m.group('title')

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("{0} URL\n".format(sys.argv[0]))
        sys.exit(1)

    url = sys.argv[1]
    title = get_page_title(url)

    wiki_api = wiki.API('wikipedia')
    #ganfyd_api = wiki.API('ganfyd')

    #obj = wiki_api.query_categories(title)
    obj = wiki_api.get_page_categories(title)

    json.dump(obj, sys.stdout, indent=2)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()
