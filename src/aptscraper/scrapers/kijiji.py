import logging
import requests
import re

from . import utils


HOME = 'http://www.kijiji.ca'


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
    apt = {}
    apt['dims'] = None

    title_div = soup.find('div', {'itemtype': 'http://schema.org/Product'})
    apt['title'] = title_div.get_text().strip()

    attrs = soup.find('table', class_='ad-attributes')
    price = attrs.find('span', {'itemprop': 'price'}).get_text()
    price = ''.join(re.findall(r'(\d|\.)', price.replace(',', '.')))
    apt['price'] = float(price)

    apt['body'] = '\n'.join(soup.find(id='UserContent').stripped_strings)
    shown_image = soup.find(id='ShownImage')
    images = []
    if shown_image:
        lis = shown_image.find_all('li', recursive=False)
        for li in lis:
            img = li.find('img', recursive=False)
            if not img:  # is a video
                continue
            link = li.find('img')['src']
            parts = link.split('/')
            root = parts[:-1]
            fname = parts[-1]
            if not fname.startswith('$'):
                images.append(link)
                continue
            base, ext = fname.split('.')
            new_fname = '.'.join(['$_27', ext])
            images.append('/'.join(root + [new_fname, ]))

    apt['images'] = images
    head = soup.head
    lat = lng = None
    apt['geo'] = None
    for meta in head.find_all('meta'):
        try:
            prop = meta['property']
        except KeyError:
            continue
        if prop == 'og:latitude':
            lat = float(meta['content'])
        elif prop == 'og:longitude':
            lng = float(meta['content'])

        # Does not enter for lat = lng = 0.0. OK
        if lat and lng:
            apt['geo'] = (lat, lng)
            break

    return apt
