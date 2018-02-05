import os
import pytest
import unittest.mock

from donna.core import database, factory, network

from . import samples


@pytest.fixture(scope='function')
def db():
    client = factory.create_client()
    database.init_db(client)
    db = database.get_db()
    yield
    client.drop_database(db)


@pytest.fixture(scope='function')
def job():
    return database.Job(
        queries=["hello.com"],
        hoods=None,
        to_email="me@test.org"
    )


@pytest.fixture(scope='function')
def history(db, job):
    job_id = database.add_job(job)
    return database.ScrapeHistory(job_id)


real = pytest.mark.skipif(
    not os.environ.get('REAL_SCRAPE', '') == 'TRUE',
    reason='Local only'
)


@pytest.fixture(scope='function')
def patch_network(monkeypatch):
    mock = unittest.mock.Mock(side_effect=_mocked_get)
    monkeypatch.setattr(network, 'get', mock)
    return mock


def parse(fpath):
    from donna.core import parser
    return parser.parse(open(fpath).read())


def _mocked_get(url):
    print('mocked get ' + url)
    fpath = _get_fpath_for_url(url)
    return _MockedResponse(fpath)


class _MockedResponse():
    def __init__(self, fpath):
        assert os.path.exists(fpath)
        with open(fpath, 'rb') as f:
            self.content = f.read()
        self.text = self.content.decode()
        self.ok = True


def _get_fpath_for_url(url):
    for search_pages in samples.SEARCH_PAGES.values():
        for search_page in search_pages:
            if url == search_page['url']:
                return search_page['fpath']

    raise AssertionError('Invalid url %s' % url)
