def extract_next_page(soup):
    """
    Extract "href" to next page given current page.
    """
    link = soup.head.find('link', rel='next')
    return link['href'] if link is not None else None


def scrape_listings(soup):
    """
    Reposts are returned with their original `ad_id`.
    """
    ul = soup.find('ul', class_='rows')
    lis = ul.find_all('li', class_='result-row', recursive=False)
    ret = []
    for li in lis:
        a = li.find('a', class_='result-title')
        ad_id = li.get('data-repost-of') or li.get('data-pid')
        ret.append({
            'ad_id': ad_id,
            'href': a.get('href'),
            'title': a.get_text(),
        })

    return ret


def scrape_ad(soup):
    ad = {
        'body': '',
        'geo': {
            'lat': None,
            'lng': None,
            'address': None,
        },
        'images': [],
        'price': None,
        'title': '',
    }
    header = soup.find(class_='postingtitle')
    price = header.find(class_='price')
    if price:
        price = float(price.get_text().replace('$', '').strip())
    ad['price'] = price
    ad['title'] = header.find(id='titletextonly').get_text()
    body = soup.find(id='postingbody')
    try:
        body.div.extract()
    except:
        pass
    ad['body'] = '\n'.join(body.stripped_strings)
    thumbs = soup.find(id='thumbs')
    images = []
    if thumbs:
        images = [thumb['href'] for thumb in thumbs.find_all('a', recursive=False)]
    else:
        swipe = soup.find(class_='swipe')
        if swipe:
            images = [swipe.find('img')['src']]

    ad['images'] = images
    map_and_attrs = soup.find(class_='mapAndAttrs')
    lat = lng = address = None
    mapdiv = map_and_attrs.find(id='map')
    if mapdiv:
        lat = float(mapdiv['data-latitude'])
        lng = float(mapdiv['data-longitude'])
    mapaddress = map_and_attrs.find(class_='mapaddress')
    if mapaddress:
        address = mapaddress.get_text()
    ad['geo'] = {
        'lat': lat,
        'lng': lng,
        'address': address,
    }
    return ad
