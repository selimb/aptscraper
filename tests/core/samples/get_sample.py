import datetime
import requests
import sys

url, fname = sys.argv[1:3]
open(fname, 'w').write(requests.get(url).text)
entry = '[{date}] {url} -> {fname}\n'.format(
    date=datetime.datetime.now().date().isoformat(),
    url=url,
    fname=fname
)
open('history.txt', 'a').write(entry)
