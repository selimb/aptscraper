from urllib.parse import urlparse, urljoin


AVAILABLE_SCRAPERS = [
    'kijiji',
    'craigslist',
]


def infer_scraper(base_query_url):
    netloc = urlparse(base_query_url).netloc
    return next(
        (scraper for scraper in AVAILABLE_SCRAPERS if scraper in netloc),
        None
    )


def href_to_abs(base_query_url, href):
    return urljoin(base_query_url, href)
