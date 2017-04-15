import bs4
from urllib.parse import urlencode

PARSER_LIB = 'html.parser'


def construct_url(path, params):
    parts = [path]
    if params:
        parts.append(urlencode(params, doseq=True))

    return '?'.join(parts)


def mk_soup(html):
    return bs4.BeautifulSoup(html, PARSER_LIB)
