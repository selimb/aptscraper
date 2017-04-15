import json
import os
import pytest
import random
import requests

import aptscraper.config


TEST_DIR = os.path.dirname(__file__)
SAMPLE_DIR = 'sample'


real = pytest.mark.skipif(
    not os.environ.get('REAL_SCRAPE', '') == 'TRUE',
    reason='Local only'
)


class MonkeyResponse(object):
    def __init__(self, fpath):
        self.text = open(fpath).read()
        self.ok = True


@pytest.fixture()
def patch_request(monkeypatch):
    monkeypatch.setattr(requests, 'get', MonkeyResponse)


def sample_fpath_factory(dname):
    def wrapped(fname):
        fpath = os.path.join(TEST_DIR, SAMPLE_DIR, dname, fname)
        return fpath
    return wrapped


def assert_no_duplicates(listings):
    unique_ids = {l['data_id'] for l in listings}
    assert len(listings) == len(unique_ids)


def assert_apt(apt, expected):
    if 'num_images' in expected:
        assert len(set(apt['images'])) == expected.pop('num_images')
    if 'body_sub' in expected:
        assert expected.pop('body_sub') in apt['body']
    for key in expected:
        assert apt[key] == expected[key]


@pytest.fixture(scope='function')
def newconf(tmpdir):
    def wrapped(dct):
        tmpdir.chdir()
        tmpdir.join('conf.json').write(json.dumps(dct))
        return aptscraper.config.init_conf('.')
    return wrapped


@pytest.fixture(scope='function')
def scraper_integration(newconf):
    def wrapped(scraper):
        min_count = 210
        min_price = 1200
        max_price = 1500
        conf = newconf(dict(
            min_price=min_price,
            max_price=max_price
        ))
        listings = scraper.collect_listings(
            min_count,
            conf
        )
        assert len(listings) >= min_count
        with_geo = 0
        for listing in random.sample(listings, 10):
            url = listing['url']
            r = requests.get(url)
            assert r.ok
            apt = scraper.parse_posting(r.text)
            assert apt
            if apt['geo']:
                with_geo += 1
            price = apt['price']
            assert price >= min_price and price <= max_price
            for image in apt['images']:
                r = requests.get(image)
                assert r.ok

        assert with_geo >= 1

    return wrapped
