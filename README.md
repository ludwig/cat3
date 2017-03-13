# Notes

Setting up a local `venv`

    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt

This seems to work in a wiki page, using the preloaded jquery,

    $.map($('#catlinks a'), function(val,i) { return val.href; })

A similar script for scraping those catlinks (skipping hidden categories this time):

    ./scrape-page-catlinks.py https://en.wikipedia.org/wiki/Heart

Samme, but using the Wikipedia API instead of scraping,

    ./get-page-categories.py https://en.wikipedia.org/wiki/Heart

To get the subcategories of a given category (spaces and underscores are equivalent):

    ./get-subcat.py "Cardiac anatomy"
    ./get-subcat.py Cardiac_anatomy
    ./get-subcat.py Liver
    ./get-subcat.py Hepatology
    ./get-subcat.py Diseases_of_liver

