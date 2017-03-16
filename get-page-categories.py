#!/usr/bin/env python3

import sys
import re
import json
import wiki

from urllib.parse import urlparse

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

    #obj = wiki.query_categories(title)
    obj = wiki.get_page_categories(title)

    json.dump(obj, sys.stdout, indent=2)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()
