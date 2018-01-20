from functools import partial
from os.path import dirname, join


SAMPLES_DIR = dirname(__file__)


def get_sample(scraper_name, fname):
    return join(SAMPLES_DIR, scraper_name, fname)


kijiji = partial(get_sample, 'kijiji')
craigslist = partial(get_sample, 'craigslist')


SEARCH_PAGES = {
    # kijiji scraper should skip "Top Ads"
    'kijiji': [
        {
            'fpath': kijiji('search_0.html'),
            'url': 'https://www.kijiji.ca/b-logiciels/ville-de-montreal/c786l1700281?price=30__100&minNumberOfImages=1',  # noqa
            'num_listings': 18,
            'first_expected': {
                'href': '/v-logiciels/ville-de-montreal/roku-mag-254-talfaza-fsat-fibersat-boxyhd-smart-iptv/1201733436',  # noqa
                'url': 'https://www.kijiji.ca/v-logiciels/ville-de-montreal/roku-mag-254-talfaza-fsat-fibersat-boxyhd-smart-iptv/1201733436',  # noqa
            },
        },
        {
            'fpath': kijiji('search_1.html'),
            'url': 'https://www.kijiji.ca/b-logiciels/ville-de-montreal/page-2/c786l1700281?price=30__100&minNumberOfImages=1',  # noqa
            'num_listings': 18,
            'first_expected': {
                'href': '/v-logiciels/ville-de-montreal/dreamweaver-cd-version-francaise/1307396690',  # noqa
                'url': 'https://www.kijiji.ca/v-logiciels/ville-de-montreal/dreamweaver-cd-version-francaise/1307396690',  # noqa
            },
        },
        {
            'fpath': kijiji('search_2.html'),
            'url': 'https://www.kijiji.ca/b-logiciels/ville-de-montreal/page-3/c786l1700281?price=30__100&minNumberOfImages=1',  # noqa
            'num_listings': 18,  # kijiji fails at counting...
            'first_expected': {
                'href': '/v-logiciels/ville-de-montreal/logiciel-microsoft-visio-2016-en-version-digitale/1301387949',  # noqa
                'url': 'https://www.kijiji.ca/v-software/ville-de-montreal/logiciel-microsoft-visio-2016-en-version-digitale/1301387949',  # noqa
            }
        }
    ],
    'craigslist': [
        {
            'fpath': craigslist('search_0.html'),
            'url': 'https://montreal.craigslist.ca/search/bik',
            'num_listings': 120,
            'first_expected': {
                'href': 'https://montreal.craigslist.ca/bik/d/teenager-mountain-bike/6381884696.html',  # noqa
            }
        },
        {
            'fpath': craigslist('search_1.html'),
            'url': 'https://montreal.craigslist.ca/search/bik?s=120',
            'num_listings': 120,
            'first_expected': {
                'href': 'https://montreal.craigslist.ca/bik/d/peugeot-avec-mise-au-point-et/6329761770.html',  # noqa
            }
        },
        {
            'fpath': craigslist('search_2.html'),
            'url': 'https://montreal.craigslist.ca/search/bik?s=240',
            'num_listings': 14,
            'first_expected': {
                'href': 'https://montreal.craigslist.ca/bik/d/nice-fixed-gear-pignon-fixe/6289089051.html'  # noqa
            }
        }
    ]
}
for page in SEARCH_PAGES['craigslist']:
    fexp = page['first_expected']
    fexp['url'] = fexp['href']


EXPECTED_ADS = {
    'kijiji': [
        ('posting.html', {
            'title': 'Table de Poker Professionnelle',
            'price': 600.0,
            'body_pattern': 'Véritables jetons de casino.\nBelle lampe de table casino.',
            'images': [
                'https://i.ebayimg.com/00/s/NDUwWDgwMA==/z/iv8AAOSwdDtZusaK/$_57.JPG',
                'https://i.ebayimg.com/00/s/ODAwWDQ1MA==/z/pdwAAOSwNJ9ZusZ4/$_57.JPG',
                'https://i.ebayimg.com/00/s/NDUwWDgwMA==/z/-YMAAOSwiOdZusad/$_57.JPG',
                'https://i.ebayimg.com/00/s/NDUwWDgwMA==/z/CVkAAOSwCY9Zusax/$_57.JPG',
            ],
            'geo': {
                'lat': 45.5543497,
                'lng': -73.21421529999999,
                'address': 'Beloeil, QC J3G3R2',
            },
        }),
        ('posting_no_picture.html', {
            'images': [],
        }),
        ('posting_no_price.html', {
            'price': None,
        }),
        ('posting_no_price.html', {
            'geo': {
                'lat': None,
                'lng': None,
                'address': None,
            },
        }),
    ],
    'craigslist': [
        ('posting.html', {
            'title': 'Lasalle 2 1/2 - for rent',
            'price': 550,
            'geo': {
                'lat': 45.418760,
                'lng': -73.625754,
                'address': '8809 Beyries',
            },
            'images': [
                'https://images.craigslist.org/00w0w_kEov2CNSGP4_600x450.jpg',
                'https://images.craigslist.org/00q0q_c9xCK5LHR4U_600x450.jpg',
                'https://images.craigslist.org/00F0F_gKxNg9NHeaR_600x450.jpg',
                'https://images.craigslist.org/01515_elxxzhl92hf_600x450.jpg',
                'https://images.craigslist.org/00J0J_e8vLRfSmLkt_600x450.jpg',
                'https://images.craigslist.org/00606_c3iZwr957Y7_600x450.jpg',
            ],
            'body_pattern': 'Planchers en bois franc. Cuisine neuve.',
        }),
        ('posting_not_apartment.html', {
            'title': '2010 Piaggio MP3 Scooter.',
            'num_images': 5,
            'body_pattern': 'Runs Like New.\nIn order to drive bike',
            'price': 3295,
        }),
        ('posting_single-picture.html', {
            'title': 'Vous etes prêt a acheter? Nous reprenons votre bail!',
            'price': None,
            'num_images': 1,
            'body_pattern': 'QC H3B\nVous êtes prêt à acheter,',
        }),
        ('posting_no-map.html', {
            'geo': {
                'lat': None,
                'lng': None,
                'address': None,
            },
        }),
        ('posting_no-picture.html', {
            'images': [],
        }),
    ],
}
