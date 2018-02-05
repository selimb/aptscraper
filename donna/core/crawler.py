"""
The grand orchestrator.

Knows about everything.
"""
import itertools
import logging
from urllib.parse import urljoin

from . import (
    network,
    parser,
    scrapers
)


# Very arbitrary
MIN_COUNT = 200


def crawl(base_url, hoods, to_email, history):
    logger = logging.get_logger(__name__)
    logger.info('Crawling ' + base_url)
    scraper = _infer_scraper(base_url)
    ad_urls = collect_ad_urls(base_url, scraper)
    unvisited_urls = filter_new_urls(ad_urls, history)
    raise NotImplementedError
    logger.info('Found %i new ads' % len(unvisited_urls))
    ads = collect_ads(ad_urls, scraper)
    for ad in ads:
        if hoods:
            geo = ad['geo']
            lat, lng = geo['lat'], geo['lng']
            hood = match_hood(lat, lng, hoods)
            if not hood:
                mark_visited(ad, history)
                continue

            ad['hood'] = hood

        send_ad(ad)
        mark_visited(ad)


def collect_ad_urls(base_url, scraper, min_count):
    ret = []
    next_page_url = base_url
    count = 0
    while next_page_url is not None and count < min_count:
        page = network.get(next_page_url).text
        soup = parser.parse(page)
        listings = scraper.scrape_listings(soup)
        ret.extend([
            _href_to_abs(base_url, listing['href'])
            for listing in listings
        ])
        count = len(ret)
        next_page_url = scraper.extract_next_page(soup)

    return ret


def filter_new_urls(urls, history):
    visited = history.was_visited(urls)
    return [url for i, url in enumerate(urls) if not visited[i]]


def collect_ads(urls, scraper):
    pass


def match_hood(lat, lng, hoods):
    pass


def mark_checked(ad, history):
    pass


def send_ad(ads):
    pass


def _infer_scraper(base_query_url):
    netloc = urlparse(base_query_url).netloc
    try:
        scraper_name = next(name for name in scrapers.AVAILABLE_SCRAPERS if name in netloc)
    except StopIteration:
        raise NotImplementedError("No scraper available for url " + base_query_url)

    return scrapers.get_scraper(scraper_name)


def _href_to_abs(base_query_url, href):
    return urljoin(base_query_url, href)

