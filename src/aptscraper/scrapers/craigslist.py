import logging
import requests

from . import utils

HOME = 'https://montreal.craigslist.ca'


def collect_listings(min_count, conf):
    return _collect_listings(
        min_count,
        min_price=conf.get('min_price'),
        max_price=conf.get('max_price'),
        laundry=conf.get('laundry'),
    )


def _collect_listings(min_count, *, min_price, max_price, laundry):
    logger = logging.getLogger()
    listings = []
    num = 0
    while num <= min_count:
        url = construct_search_url(
            start=num,
            min_price=min_price,
            max_price=max_price,
            laundry=laundry
        )
        logger.info('SCRAPING: %s' % url)
        page = requests.get(url).text
        items = extract_items(page)
        for item in items:
            data_id = item['repost'] or item['data_id']
            url = HOME + item['href']
            listings.append({
                'data_id': data_id,
                'url': url,
                'title': item['title'],
            })

        num = len(listings)

    return listings


def construct_search_url(*, start, min_price, max_price, laundry):
    path = HOME + '/search/apa'
    params = dict(
        sort='date',
        availabilityMode='0',
    )
    if start:
        params['s'] = start
    if min_price:
        params['min_price'] = min_price
    if max_price:
        params['max_price'] = max_price
    if laundry:
        params['laundry'] = [1, 4]

    return utils.construct_url(path, params)


def extract_items(html):
    logger = logging.getLogger()
    soup = utils.mk_soup(html)
    ul = soup.find('ul', class_='rows')
    lis = ul.find_all('li', class_='result-row', recursive=False)
    logger.info('Found %d items.' % len(lis))
    listings = []
    for li in lis:
        a = li.find('a', class_='result-title')
        listings.append({
            'data_id': li.get('data-pid'),
            'repost': li.get('data-repost-of'),
            'href': a.get('href'),
            'title': a.get_text(),
        })

    return listings


def parse_posting(html):
    soup = utils.mk_soup(html)
    apt = {}
    header = soup.find(class_='postingtitle')
    dims = None
    price = header.find(class_='price')
    if price:
        price = float(price.get_text().replace('$', '').strip())
    apt['price'] = price
    dims = header.find(class_='housing')
    if dims:
        dims = dims.get_text().strip()
        if dims.startswith('/'):
            dims = dims[1:].strip()
        if dims.endswith('-'):
            dims = dims[:-1].strip()
    apt['dims'] = dims
    apt['title'] = header.find(id='titletextonly').get_text()
    body = soup.find(id='postingbody')
    try:
        body.div.extract()
    except:
        pass
    apt['body'] = '\n'.join(body.stripped_strings)
    thumbs = soup.find(id='thumbs')
    images = []
    if thumbs:
        for thumb in thumbs.find_all('a', recursive=False):
            images.append(thumb['href'])
    else:
        swipe = soup.find(class_='swipe')
        if swipe:
            img = swipe.find('img')
            images.append(img['src'])

    apt['images'] = images
    mapdiv = soup.find(id='map')
    geo = None
    if mapdiv:
        lat = float(mapdiv['data-latitude'])
        lng = float(mapdiv['data-longitude'])
        geo = (lat, lng)
    apt['geo'] = geo
    return apt
