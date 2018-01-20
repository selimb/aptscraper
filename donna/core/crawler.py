"""
The grand orchestrator.

Knows about everything.
"""
from urllib.parse import urljoin

from . import (
    network,
    parser
)


# Very arbitrary
MIN_COUNT = 200


def crawl(base_url, hoods, to_email, scraper, store):
    raise NotImplementedError
    ad_urls = collect_ad_urls(base_url, scraper)
    unvisited_urls = filter_visited(ad_urls, store)
    ads = collect_ads(ad_urls, scraper)
    for ad in ads:
        if hoods:
            geo = ad['geo']
            lat, lng = geo['lat'], geo['lng']
            hood = match_hood(lat, lng, hoods)
            if not hood:
                mark_visited(ad, store)                
                continue
            
            ad['hood'] = hood
        
        send_ad(ad)
        mark_visited(ad)
    pass


def collect_ad_urls(base_url, scraper, min_count):
    ret = []
    next_page_url = base_url
    count = 0
    while next_page_url is not None:# and count < min_count:
        page = network.get(next_page_url).text
        soup = parser.parse(page)
        listings = scraper.scrape_listings(soup)
        ret.extend([
            _href_to_abs(base_url, listing['href'])
            for listing in listings
        ])
        next_page_url = scraper.extract_next_page(soup)
    
    return listings


def filter_new_listings(listings, store):
    pass


def collect_ads(listings, scraper):
    pass


def match_hood(lat, lng, hoods):
    pass


def mark_checked(ad, store):
    pass


def send_ads(ads):
    pass


def infer_scraper(base_query_url):
    netloc = urlparse(base_query_url).netloc
    return next(
        (scraper for scraper in AVAILABLE_SCRAPERS if scraper in netloc),
        None
    )


def _href_to_abs(base_query_url, href):
    return urljoin(base_query_url, href)
