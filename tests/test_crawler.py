from unittest.mock import call
import pytest

def test_collect_search_results_kijiji():
    return
    sample_fpath = sample_fpath_factory('kijiji')
    fpaths = [sample_fpath('search_%d.html' % i) for i in range(3)]
    requests_mock = patch_requests(fpaths)

    crawler = AdCrawler(scrapers.kijiji)
    # Obtained from history
    expected_urls = [
        'https://www.kijiji.ca/b-appartement-condo-studio-2-1-2/ville-de-montreal/c212l1700281?minNumberOfImages=1', # noqa
        'https://www.kijiji.ca/b-appartement-condo-studio-2-1-2/ville-de-montreal/page-2/c212l1700281?minNumberOfImages=1', # noqa
        'https://www.kijiji.ca/b-appartement-condo-studio-2-1-2/ville-de-montreal/page-3/c212l1700281?minNumberOfImages=1', # noqa
    ]
    search_results = crawler.collect_search_results(expected_urls[0], 50)
    assert requests_mock.call_count == 3
    requests_mock.assert_has_calls([call(url) for url in expected_urls])
    assert len(search_results) == 60
    expected = {
        23: {
            'data_id': '1296843490',
            'href': '/v-appartement-condo-studio-2-1-2/ville-de-montreal/spacious-one-bedroom-monkland-n-d-g/1296843490',
            'title': 'SPACIOUS ONE BEDROOM MONKLAND N.D.G',
        }
    }
    assert_search_results(search_results, expected)

