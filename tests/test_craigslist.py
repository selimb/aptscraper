import requests

import pytest

from aptscraper.scrapers import craigslist as scraper

from .conftest import (
    sample_fpath_factory,
    real,
    assert_no_duplicates,
    assert_apt
)


sample_fpath = sample_fpath_factory('craigslist')


@real
def test_all(scraper_integration):
    scraper_integration(scraper)


@real
@pytest.mark.parametrize('min_price', [None, 800])
@pytest.mark.parametrize('max_price', [None, 1300])
@pytest.mark.parametrize('laundry', [False, True])
@pytest.mark.parametrize('start', [None, 0, 150])
def test_urls_valid(min_price, max_price, laundry, start):
    url = scraper.construct_search_url(**locals())
    r = requests.get(url)
    assert r.ok
    listings = scraper.extract_items(r.text)
    assert listings


def test_collect_listings(monkeypatch, patch_request):
    called_with = []

    def monkey_url(**kwargs):
        start = kwargs['start']
        template = 'search_{:d}.html'
        called_with.append(start)
        if start == 0:
            return sample_fpath(template.format(0))
        elif start == 120:
            return sample_fpath(template.format(120))
        else:
            raise AssertionError('Invalid start {}'.format(start))

    monkeypatch.setattr(scraper, 'construct_search_url', monkey_url)
    listings = scraper._collect_listings(
        200,
        min_price=None,
        max_price=None,
        laundry=None
    )
    assert len(listings) == 240
    assert called_with == [0, 120]
    listing = listings[0]
    assert listing['url'] == 'https://montreal.craigslist.ca/apa/6102413505.html'
    assert listing['title'] == 'Ecole polythechnic, HEC, UdM Nice 2,5'
    # Is a repost
    listing = listings[6]
    assert listing['data_id'] == '4898502273'
    assert listing['url'] == 'https://montreal.craigslist.ca/apa/6075329741.html'
    assert listing['title'] == '!!!!!!!!!!!!!!!!!!NEWLY RENOVATE 3.5 NEAR UNIVERSITY  HEC!!!!!!!!!!!!!' # noqa
    listing = listings[119 + 21]
    assert listing['data_id'] == '5962018650'
    assert listing['title'] == 'Downtown luxury building - ideal for Professionals & grad students'


def test_extract_items():
    page = open(sample_fpath('search.html')).read()
    listings = scraper.extract_items(page)
    assert len(listings) == 120
    assert_no_duplicates(listings)
    expected = {
        0: {
            'data_id': '6095456551',
            'repost': None,
            'href': '/apa/6095456551.html',
            'title': 'RenovatedSemi-Basement Apartment on Beaubien Street',
        },
        10: {
            'data_id': '6075485539',
            'repost': '4875783066',
            'href': '/apa/6075485539.html',
            'title': 'Beautiful 7½ close to McGill Sports Centre,Cegep,Jeanne-Mance Park',
        }
    }
    for idx in expected.keys():
        assert expected[idx] == listings[idx]


@pytest.mark.parametrize('fname, expected', [
    ('posting.html', {
        'title': '2000 Square Feet Renovated Apartment in Verdun',
        'price': 2200,
        'dims': '4br',
        'geo': (45.450290, -73.576727),
        'num_images': 15,
        'body_sub': '601 Moffat, Verdun H4H-1Y7\n$2200/month-available as of  July 1\nSpacious',
    }),
    ('posting_single-picture.html', {
        'title': 'Vous etes prêt a acheter? Nous reprenons votre bail!',
        'price': None,
        'dims': None,
        'num_images': 1,
        'body_sub': 'QC H3B\nVous êtes prêt à acheter,',
    }),
    ('posting_no-map.html', {
        'geo': None,
    }),
    ('posting_map-is-area.html', {
        'geo': (45.578000, -73.800400),
        'dims': '1br - 840ft2',
    }),
    ('posting_no-picture.html', {
        'num_images': 0,
    }),
])
def test_parse_posting(fname, expected):
    page = open(sample_fpath(fname)).read()
    apt = scraper.parse_posting(page)
    assert_apt(apt, expected)
