import bs4


# TODO: Change this to lxml
PARSER_LIB = 'html.parser'


def parse(html):
    return bs4.BeautifulSoup(html, PARSER_LIB)


