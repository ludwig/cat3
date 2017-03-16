#!/usr/bin/env python3

import sys
import json
import wiki

# Example query: https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtype=subcat&cmtitle=Category:Anatomy

def main():
    if len(sys.argv) < 2:
        # NOTE: The category can be specified with either spaces or underscores.
        sys.stderr.write("{0} CATEGORY\n".format(sys.argv[0]))
        sys.exit(1)

    category = sys.argv[1]

    #obj = wiki.query_subcat(category)
    obj = wiki.get_subcategories(category)

    json.dump(obj, sys.stdout, indent=2)
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()
