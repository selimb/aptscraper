import pytest

from tarantule.core.scrapers import kijiji as scraper

from .conftest import sample_fpath_factory, assert_ad, parse


sample_fpath = sample_fpath_factory('kijiji')


def test_extract_next_page_when_on_last_page():
    soup = parse(sample_fpath('search_last_page.html'))
    next_page_url = scraper.extract_next_page(soup)
    assert next_page_url is None


def test_extract_next_page():
    soup = parse(sample_fpath('search.html'))
    next_page_url = scraper.extract_next_page(soup)
    assert next_page_url == 'https://www.kijiji.ca/b-achat-et-vente/ville-de-montreal/velo/page-2/k0c10l1700281' # noqa


@pytest.mark.parametrize('top', [False, True])
def test_scrape_listings(top):
    soup = parse(sample_fpath('search.html'))
    listings = scraper.scrape_listings(soup, top=top)
    expected_length = 25 if top is True else 20
    offset = 0 if top is True else 5
    assert len(listings) == expected_length
    # Expected includes top
    expected_listings = {
        0: {
            'ad_id': '1256565383',
            'href': '/v-de-plage-urbain-hybride/ville-de-montreal/velo-hybride-performance-transit-1-0-2017-special/1256565383', # noqa
            'title': 'Vélo hybride performance Transit 1.0 2017 - SPECIAL !!',
        },
        6: {
            'ad_id': '1294788259',
            'href': '/v-de-plage-urbain-hybride/ville-de-montreal/velo-urbain-retro/1294788259', # noqa
            'title': 'Vélo urbain retro',
        },
        24: {
            'ad_id': '1294779103',
            'href': '/v-autres-velo/ville-de-montreal/velo-bicyclette-louis-garneau/1294779103', # noqa
            'title': 'Vélo/ bicyclette louis garneau',
        },
    }
    for key, expected in expected_listings.items():
        idx = key - offset
        if idx < 0:
            continue
        assert expected == listings[idx]


@pytest.mark.parametrize('fname, expected', [
    ('posting.html', {
        'title': 'Table de Poker Professionnelle',
        'price': 600.0,
        'body_pattern': 'Véritables jetons de casino.\nBelle lampe de table casino.',
        'images': [
             'https://i.ebayimg.com/00/s/NDUwWDgwMA==/z/iv8AAOSwdDtZusaK/$_57.JPG',
             'https://i.ebayimg.com/00/s/ODAwWDQ1MA==/z/pdwAAOSwNJ9ZusZ4/$_57.JPG',
             'https://i.ebayimg.com/00/s/NDUwWDgwMA==/z/-YMAAOSwiOdZusad/$_57.JPG',
             'https://i.ebayimg.com/00/s/NDUwWDgwMA==/z/CVkAAOSwCY9Zusax/$_57.JPG',
        ],
        'geo': {
            'lat': 45.5543497,
            'lng': -73.21421529999999,
            'address': 'Beloeil, QC J3G3R2',
        },
    }),
    ('posting_no_picture.html', {
        'images': [],
    }),
    ('posting_no_price.html', {
        'price': None,
    }),
    ('posting_no_price.html', {
        'geo': {
            'lat': None,
            'lng': None,
            'address': None,
        },
    }),
])
def test_scrape_ad(fname, expected):
    soup = parse(sample_fpath(fname))
    ad = scraper.scrape_ad(soup)
    assert_ad(ad, expected)
