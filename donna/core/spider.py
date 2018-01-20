
from tarantule.core.parser import parse
from tarantule.core.geo import is_point_inside_polygon
from . import network

def setup_spider():
    raise NotImplementedError



class Spider:

    MIN_COUNT = 200

    def __init__(self, base_query_url, hoods, scraper, store):
        self.base_query_url = base_query_url
        self.scraper = scraper
        self.db = db

    def collect_listings(self):

    def collect_search_results(self, base_url, min_count):
        logger = logging.getLogger()
        ret = []
        url = base_url
        while len(ret) < min_count and url is not None:
            logger.info('GET %s' % url)
            html = network.get(url).text
            soup = mk_soup(html)
            ret.extend(self.scraper.scrape_search_results(soup))
            url = self.scraper.extract_next_page(soup)

        return ret

