import pytest
import requests

from donna.core import engine

responses = {
    'url_0': [
        {
            'data_id':
    ]
}
@pytest.fixture()
def patch_request(monkeypatch):
    monkeypatch.setattr(requests, 'get', lambda url: responses[url])
def test_collect_listings():

