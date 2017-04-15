import os
import pytest
import requests

from aptscraper.scrapers import kijiji as scraper

from .conftest import (
    sample_fpath_factory,
    real,
    assert_no_duplicates,
    assert_apt
)


sample_fpath = sample_fpath_factory('kijiji')


@real
def test_all(scraper_integration):
    scraper_integration(scraper)


@real
@pytest.mark.parametrize('min_price', [None, 800])
@pytest.mark.parametrize('max_price', [None, 1300])
@pytest.mark.parametrize('page', [1, 5])
def test_urls(min_price, max_price, page):
    url = scraper.construct_search_url(**locals())
    page = 'page-%d' % page
    assert page in url
    if min_price:
        assert str(min_price) in url
    if max_price:
        assert str(max_price) in url
    r = requests.get(url)
    assert r.ok
    listings = scraper.extract_items(r.text)
    assert listings


def test_collect_listings(monkeypatch, patch_request):
    called_with = []

    def monkey_url(**kwargs):
        page = kwargs['page']
        called_with.append(page)
        fpath = sample_fpath('search_%d.html' % page)
        assert os.path.exists(fpath)
        return fpath

    monkeypatch.setattr(scraper, 'construct_search_url', monkey_url)
    listings = scraper._collect_listings(
        55,
        min_price=None,
        max_price=None,
    )
    assert len(listings) == 60
    assert called_with == [1, 2, 3]


def test_extract_items():
    page = open(sample_fpath('search.html')).read()
    listings = scraper.extract_items(page)
    assert len(listings) == 25
    top_listings = [l for l in listings if l['is_top']]
    assert len(top_listings) == 5
    assert top_listings == listings[:5]
    assert_no_duplicates(listings)
    expected = {
        0: {
            'data_id': '1256508533',
            'is_top': True,
            'href': '/v-appartement-condo-4-1-2/ville-de-montreal/1-mois-gratuit-offert-en-avril/1256508533?src=topAdSearch', # noqa
            'title': '1 MOIS GRATUIT, OFFERT EN AVRIL',
        },
        6: {
            'data_id': '1257197018',
            'is_top': False,
            'href': '/v-appartement-condo-studio-2-1-2/ville-de-montreal/beautiful-3-1-2-for-rent-in-ville-lasalle/1257197018', # noqa
            'title': 'Beautiful 3 1/2 for rent in Ville Lasalle',
        },
    }
    for idx in expected.keys():
        assert expected[idx] == listings[idx]


@pytest.mark.parametrize('fname, expected', [
    ('posting.html', {
        'title': '3 1/2 a louer',
        'price': 650,
        'dims': None,
        'geo': (45.5379203, -73.6735446),
        'num_images': 6,
        'body_sub': '3 1/2 av.du Bois de Boulogne\nBeau 3 1/2',
    }),
    ('posting_no-picture.html', {
        'title': '5 1/2 a louer Anjou coin Roi Rene - Wilfrid Pelletier',
        'num_images': 0,
    }),
    ('posting_map-is-area.html', {
        'title': 'Très grand 4½ lumineux, secteur Mercier-Hochelaga-Maisonneuve',
        'geo': (45.5691597, -73.5239224),
    }),
])
def test_parse_posting(fname, expected):
    page = open(sample_fpath(fname)).read()
    apt = scraper.parse_posting(page)
    assert_apt(apt, expected)
