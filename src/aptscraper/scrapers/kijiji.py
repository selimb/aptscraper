import logging
import requests
import json
import html as html_utils
import re

from . import utils


HOME = 'http://www.kijiji.ca'
_IMG_REGEX = re.compile('\$_\d+\.JPG')


def collect_listings(min_count, conf):
    return _collect_listings(
        min_count,
        min_price=conf.get('min_price'),
        max_price=conf.get('max_price'),
    )


def _collect_listings(min_count, *, min_price, max_price):
    logger = logging.getLogger()
    listings = []
    page_count = 0
    num = 0
    while num <= min_count:
        page_count += 1
        url = construct_search_url(
            page=page_count,
            min_price=min_price,
            max_price=max_price
        )
        logger.info('SCRAPING: %s' % url)
        page = requests.get(url).text
        items = extract_items(page)
        for item in items:
            if item['is_top']:
                continue
            url = HOME + item['href']
            listings.append({
                'data_id': item['data_id'],
                'url': url,
                'title': item['title'],
            })

        num = len(listings)

    return listings


def construct_search_url(*, page, min_price, max_price):
    path = HOME + '/b-appartement-condo/ville-de-montreal'
    path += '/page-%d' % page
    path += '/c37l1700281'
    params = dict(
        minNumberOfImages=1
    )
    if min_price or max_price:
        prices = [min_price, max_price]
        val = '__'.join('%s' % p if p else '' for p in prices)
        params['price'] = val

    return utils.construct_url(path, params)


def extract_items(html):
    soup = utils.mk_soup(html)
    items = soup.find_all('div', class_='search-item')
    listings = []
    for div in items:
        is_top = 'top-feature' in div['class']
        title_div = div.find('div', class_='title')
        listings.append({
            'data_id': div.get('data-ad-id'),
            'href': div.get('data-vip-url'),
            'is_top': is_top,
            'title': title_div.get_text().strip(),
        })

    return listings


def parse_posting(html):
    soup = utils.mk_soup(html)

    ad = {
        'images': [],
        'body': '',
        'title': '',
        'price': None,
        'geo': None,
        'dims': None,
    }
    script = soup.find(id='FesLoader').find('script').get_text()
    var, script = script.split('=', 1)
    assert var == 'window.__data'
    assert script.endswith(';')
    json_data = json.loads(script[:-1])
    json_data = json_data['config']
    ad['title'] = json_data['adInfo']['title']
    vip = json_data['VIP']
    ad['images'] = [
        _IMG_REGEX.sub('$_57.JPG', img['href'])
        for img in vip['media']
    ]
    body = html_utils.unescape(vip['description'])
    ad['body'] = _minimize_newlines(body)
    price_string = vip['price']['amount']
    if price_string is not None:
        ad['price'] = float(price_string)/100

    ad_location = vip['adLocation']
    # Kijij gives the coordinates of the area when there is no adress.
    address = ad_location.get('mapAddress')
    if address:
        lat, lng = ad_location.get('latitude'), ad_location.get('longitude')
        ad['geo'] = (lat, lng)

    return ad


def _minimize_newlines(text):
    gen = (s.strip() for s in text.split('\n') if s.strip() != '')
    return '\n'.join(gen)
