import pytest
from unittest import mock

from donna.core import crawler, scrapers

from . import samples


# Use kijiji scraper for all tests.
# Easier than using mocks, and also tests integration too.
# Would be overkill to test with all scrapers, since they should all
# have the same interface and the scrapers themselves are unit-tested.
SCRAPER = scrapers.kijiji
SEARCH_PAGES = samples.SEARCH_PAGES['kijiji']


def test_crawl(patch_network, history):
    """Functional test!"""
    HOODS = None
    TO_EMAIL = 'me@test.com'
    base_url = SEARCH_PAGES[1]['url']
    all_num_listings = [page['num_listings'] for page in SEARCH_PAGES]

    crawl(base_url, HOODS, TO_EMAIL, history)

    num_emails = None
    assert num_emails == sum(all_num_listings[1:])

    base_url = SEARCH_PAGES[0]['url']

    crawl(base_url, HOODS, TO_EMAIL, history)

    num_emails = None
    assert num_emails == all_num_listings[0]

    crawl(base_url, HOODS, TO_EMAIL, history)

    num_emails = None
    assert num_emails == 1  # Courtesy e-mail


@pytest.mark.parametrize('base_url, min_count, expected', [
    (
        SEARCH_PAGES[0]['url'],
        crawler.MIN_COUNT,
        {
            'number': sum(s['num_listings'] for s in SEARCH_PAGES),
            'num_pages': len(SEARCH_PAGES),
            'first_expected': SEARCH_PAGES[0]['first_expected']['url']
        }
    ),
    (
        SEARCH_PAGES[1]['url'],
        30,
        {
            'number': 36, # Know there's 18 per page
            'num_pages': 2,
            'first_expected': SEARCH_PAGES[1]['first_expected']['url']
        }
    ),
    (
        SEARCH_PAGES[0]['url'],
        15,
        {
            'number': SEARCH_PAGES[0]['num_listings'],
            'num_pages': 1,
            'first_expected': SEARCH_PAGES[0]['first_expected']['url'],
        }
    ),
])
def test_collect_ad_urls(patch_network, base_url, min_count, expected):
    urls = crawler.collect_ad_urls(base_url, SCRAPER, min_count)
    assert patch_network.call_count == expected['num_pages']
    assert len(urls) == expected['number']
    assert urls[0] == expected['first_expected']


def test_filter_new_urls(history):
    urls = [page["url"] for page in SEARCH_PAGES]
    assert crawler.filter_new_urls(urls, history) == urls

    history.mark_visited([urls[0]])
    assert crawler.filter_new_urls(urls, history) == urls[1:]

    history.mark_visited(urls[2:])
    assert crawler.filter_new_urls(urls, history) == [urls[1]]


def test_format_ad():
    raise NotImplementedError
