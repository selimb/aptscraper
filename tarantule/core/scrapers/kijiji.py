import json
import html
import re


_IMG_REGEX = re.compile('\$_\d+\.JPG')


def extract_next_page(soup):
    """
    Extract "href" to next page given current page.
    """
    link = soup.head.find('link', rel='next')
    return link['href'] if link is not None else None


def scrape_listings(soup, top=False):
    """
    With `top = False`, listings in the Top Ad section are ignored. See
    https://help.kijiji.ca/performance/TopAd for more information
    on Top Ads.
    """
    ret = []
    items = soup.find_all('div', class_='search-item')
    for div in items:
        listing_is_top = 'top-feature' in div['class']
        if top is False and listing_is_top:
            continue
        title_div = div.find('div', class_='title')
        ret.append({
            'ad_id': div.get('data-ad-id'),
            'href': div.get('data-vip-url'),
            'title': title_div.get_text().strip(),
        })

    return ret


def scrape_ad(soup):
    ad = {
        'images': [],
        'body': '',
        'title': '',
        'price': None,
        'geo': {
            'lat': None,
            'lng': None,
            'address': None,
        },
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
    body = html.unescape(vip['description'])
    ad['body'] = _minimize_newlines(body)
    price_string = vip['price']['amount']
    if price_string is not None:
        ad['price'] = float(price_string)/100

    ad_location = vip['adLocation']
    # Kijij gives the coordinates of the area when there is no adress.
    address = ad_location.get('mapAddress')
    if address:
        lat, lng = ad_location.get('latitude'), ad_location.get('longitude')
        ad['geo'] = {
            'lat': lat,
            'lng': lng,
            'address': address,
        }
    return ad


def _minimize_newlines(text):
    gen = (s.strip() for s in text.split('\n') if s.strip() != '')
    return '\n'.join(gen)
