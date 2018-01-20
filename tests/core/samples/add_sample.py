import datetime
import requests
import sys

if __name__ == '__main__':
    url, fname = sys.argv[1:3]
    with open(fname, 'w') as f:
        f.write(requests.get(url).content)
    entry = '[{date}] {url} -> {fname}\n'.format(
        date=datetime.datetime.now().date().isoformat(),
        url=url,
        fname=fname
    )
    with open('history.txt', 'a') as f:
        f.write(entry)
