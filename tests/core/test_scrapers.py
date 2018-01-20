import copy
import pytest

from donna.core.scrapers import AVAILABLE_SCRAPERS, get_scraper

from .conftest import assert_ad, parse
from . import samples


parametrize_scrapers = pytest.mark.parametrize(
    'scraper_name',
    ['craigslist', 'kijiji']
)



extract_next_page_params = 'scraper_name, search_page_fpath, expected_next_url'
vals = []
for scraper_name in AVAILABLE_SCRAPERS:
    search_pages = samples.SEARCH_PAGES[scraper_name]
    for idx in range(len(search_pages)):
        search_page_fpath = search_pages[idx]['fpath']
        try:
            expected_next_url = search_pages[idx + 1]['url']
        except IndexError:
            expected_next_url = None
        
        vals.append((scraper_name, search_page_fpath, expected_next_url))


@pytest.mark.parametrize(extract_next_page_params, vals)
def test_extract_next_page(scraper_name, search_page_fpath, expected_next_url):
    scraper = get_scraper(scraper_name)
    soup = parse(search_page_fpath)
    assert expected_next_url == scraper.extract_next_page(soup)


scrape_listings_params = 'scraper_name, search_page'
vals = []
for scraper_name in AVAILABLE_SCRAPERS:
    search_pages = samples.SEARCH_PAGES[scraper_name]
    vals.extend([
        (scraper_name, search_page) for search_page in search_pages
    ])


@pytest.mark.parametrize(scrape_listings_params, vals)
def test_scrape_listings(scraper_name, search_page):
    scraper = get_scraper(scraper_name)
    soup = parse(search_page['fpath'])
    listings = scraper.scrape_listings(soup)

    assert search_page['num_listings'] == len(listings)
    assert {'href': search_page['first_expected']['href']} == listings[0]


scrape_ad_params = 'scraper_name, ad_fpath, expected_ad'
vals = []
for scraper_name in AVAILABLE_SCRAPERS:
    for fname, expected_ad in samples.EXPECTED_ADS[scraper_name]:
        vals.append(
            (scraper_name, samples.get_sample(scraper_name, fname), expected_ad)
        )


@pytest.mark.parametrize(scrape_ad_params, vals)
def test_scrape_ad(scraper_name, ad_fpath, expected_ad):
    expected_ad = copy.deepcopy(expected_ad)
    scraper = get_scraper(scraper_name)
    soup = parse(ad_fpath)
    ad = scraper.scrape_ad(soup)

    if 'num_images' in expected_ad:
        assert len(set(ad['images'])) == expected_ad.pop('num_images')
    if 'body_pattern' in expected_ad:
        assert expected_ad.pop('body_pattern') in ad['body']
    for key in expected_ad:
        assert ad[key] == expected_ad[key]
