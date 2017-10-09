import os
import pytest

from tarantule.core import utils

from unittest import mock


TEST_DIR = os.path.dirname(__file__)
SAMPLES_DIR = os.path.join(TEST_DIR, 'samples')


real = pytest.mark.skipif(
    not os.environ.get('REAL_SCRAPE', '') == 'TRUE',
    reason='Local only'
)


class MockedResponse():
    def __init__(self, fpath):
        assert os.path.exists(fpath)
        self.text = open(fpath).read()
        self.ok = True


@pytest.fixture(scope='function')
def patch_requests(monkeypatch):
    """
    Returns a function that patches `requests.get` such that it returns
    the contents of the filepaths supplied to the function.

    The function returns the mock object.
    """
    # TODO: Might not need this
    def wrapped(fpaths):
        requests_mock = mock.Mock(
            side_effect=[MockedResponse(fpath) for fpath in fpaths]
        )
        monkeypatch.setattr(requests, 'get', requests_mock)
        return requests_mock
    return wrapped


def parse(fpath):
    return utils.parse(open(fpath).read())


def sample_fpath_factory(dirname):
    """
    Return a function to query path to test sample filename.
    """
    def wrapped(fname):
        fpath = os.path.join(SAMPLES_DIR, dirname, fname)
        return fpath
    return wrapped


def assert_search_results(search_results, expected):
    # TODO: Remove
    # Assert there aren't any duplicates
    unique_ids = {l['data_id'] for l in search_results}
    assert len(search_results) == len(unique_ids)
    for result in search_results:
        assert 'href' in result
        assert 'title' in result
    for idx, expected_result in expected.items():
        assert search_results[idx] == expected_result


def assert_ad(ad, expected):
    if 'num_images' in expected:
        assert len(set(ad['images'])) == expected.pop('num_images')
    if 'body_pattern' in expected:
        assert expected.pop('body_pattern') in ad['body']
    for key in expected:
        assert ad[key] == expected[key]
