from . import craigslist, kijiji


AVAILABLE_SCRAPERS = [
    'craigslist',
    'kijiji',
]


def get_scraper(scraper_name):
    assert scraper_name in AVAILABLE_SCRAPERS
    if scraper_name == 'craigslist':
        return craigslist
    if scraper_name == 'kijiji':
        return kijiji
