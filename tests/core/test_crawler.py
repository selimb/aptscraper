import pytest

from donna.core import crawler, scrapers

from . import samples


TESTED_MODULE = "donna.core.crawler"
# Use kijiji scraper for all tests.
# Easier than using mocks, and also tests integration too.
# Would be overkill to test with all scrapers, since they should all
# have the same interface.
SCRAPER = scrapers.kijiji
SEARCH_PAGES = samples.SEARCH_PAGES['kijiji']


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
            'number': 30,
            'num_pages': 2,
            'first_expected': SEARCH_PAGES[1]['first_expected']['url']
        }
    ),
])
def test_collect_ad_urls(patch_network, base_url, min_count, expected):
    urls = crawler.collect_ad_urls(base_url, SCRAPER, min_count)
    assert expected['num_pages'] == patch_network.call_count
    assert expected['number'] == len(urls)
    assert expected['first_expected'] == urls[0]
