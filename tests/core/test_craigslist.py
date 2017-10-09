import pytest

from tarantule.core.scrapers import craigslist as scraper

from .conftest import sample_fpath_factory, assert_ad, parse


sample_fpath = sample_fpath_factory('craigslist')


def test_extract_next_page_when_on_last_page():
    soup = parse(sample_fpath('search_last_page.html'))
    next_page_url = scraper.extract_next_page(soup)
    assert next_page_url is None


def test_extract_next_page():
    soup = parse(sample_fpath('search.html'))
    next_page_url = scraper.extract_next_page(soup)
    assert next_page_url == 'https://montreal.craigslist.ca/search/apa?s=120&sort=date'  # noqa


def test_scrape_listings_returns_repost_id():
    soup = parse(sample_fpath('search.html'))
    listings = scraper.scrape_listings(soup)
    expected = {
        'ad_id': '4875783066',
        'href': '/apa/6075485539.html',
        'title': 'Beautiful 7½ close to McGill Sports Centre,Cegep,Jeanne-Mance Park',
    }
    assert listings[10] == expected


def test_scrape_listings():
    soup = parse(sample_fpath('search.html'))
    listings = scraper.scrape_listings(soup)
    assert len(listings) == 120
    expected = {
        'ad_id': '6095456551',
        'href': '/apa/6095456551.html',
        'title': 'RenovatedSemi-Basement Apartment on Beaubien Street',
    }
    assert listings[0] == expected


@pytest.mark.parametrize('fname, expected', [
    ('posting.html', {
        'title': 'Lasalle 2 1/2 - for rent',
        'price': 550,
        'geo': {
            'lat': 45.418760,
            'lng': -73.625754,
            'address': '8809 Beyries',
        },
        'images': [
            'https://images.craigslist.org/00w0w_kEov2CNSGP4_600x450.jpg',
            'https://images.craigslist.org/00q0q_c9xCK5LHR4U_600x450.jpg',
            'https://images.craigslist.org/00F0F_gKxNg9NHeaR_600x450.jpg',
            'https://images.craigslist.org/01515_elxxzhl92hf_600x450.jpg',
            'https://images.craigslist.org/00J0J_e8vLRfSmLkt_600x450.jpg',
            'https://images.craigslist.org/00606_c3iZwr957Y7_600x450.jpg',
        ],
        'body_pattern': 'Planchers en bois franc. Cuisine neuve.',
    }),
    ('posting_not_apartment.html', {
        'title': '2010 Piaggio MP3 Scooter.',
        'num_images': 5,
        'body_pattern': 'Runs Like New.\nIn order to drive bike',
        'price': 3295,
    }),
    ('posting_single-picture.html', {
        'title': 'Vous etes prêt a acheter? Nous reprenons votre bail!',
        'price': None,
        'num_images': 1,
        'body_pattern': 'QC H3B\nVous êtes prêt à acheter,',
    }),
    ('posting_no-map.html', {
        'geo': {
            'lat': None,
            'lng': None,
            'address': None,
        },
    }),
    ('posting_no-picture.html', {
        'images': [],
    }),
])
def test_scrape_ad(fname, expected):
    soup = parse(sample_fpath(fname))
    ad = scraper.scrape_ad(soup)
    assert_ad(ad, expected)
