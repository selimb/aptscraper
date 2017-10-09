from tarantule.web import utils

import pytest

@pytest.mark.parametrize('base_query_url, expected', [
    (
        'https://www.kijiji.ca/b-appartement-condo-studio-2-1-2/ville-de-montreal/c212l1700281?minNumberOfImages=1', # noqa
        'kijiji'
    ),
    (
        'https://montreal.craigslist.ca/search/apa?s=120&sort=date',
        'craigslist'
    ),
    (
        'http://www.lespac.com/montreal/tables_dx0g17567k1R1.jsa',
        None
    ),
])
def test_infer_scraper(base_query_url, expected):
    assert expected == utils.infer_scraper(base_query_url)


@pytest.mark.parametrize('base_query_url, href, expected', [
    (
        'https://www.kijiji.ca/b-autos-vehicules/ville-de-montreal/c27l1700281',
        '/v-autos-camions/ville-de-montreal/2010-honda-civic-coup-tres-propre-financement-maison-39-semaine/1293354533?enableSearchNavigationFlag=true', # noqa
        'https://www.kijiji.ca/v-autos-camions/ville-de-montreal/2010-honda-civic-coup-tres-propre-financement-maison-39-semaine/1293354533?enableSearchNavigationFlag=true' # noqa
    ),
    (
        'https://seattle.craigslist.org/search/apa?hasPic=1&availabilityMode=0',
        'https://seattle.craigslist.org/tac/apa/d/650-mo-close-to-jblm/6338220649.html', # noqa
        'https://seattle.craigslist.org/tac/apa/d/650-mo-close-to-jblm/6338220649.html', # noqa
    ),
])
def test_href_to_abs(base_query_url, href, expected):
    assert expected == utils.href_to_abs(base_query_url, href)
