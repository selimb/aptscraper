"""
A driver glues pieces of the library together.
"""
from . import requests
from . import parser


def _collect_listings(scraper, base_query_url, min_count):
    ret = []
    url = base_query_url
    while len(ret) < min_count and url is not None:
        html = requests.get(url).text
        soup = parser.parse(html)
        ret.extend(self.scraper.scrape_search_results(soup))
        url = scraper.extract_next_page(soup)

    return ret


def filter_listings(listings, listings_store):
    raise NotImplementedError
