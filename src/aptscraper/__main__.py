import datetime
import logging
import logging.handlers
import os
import requests
import sys

from . import scrapers
from .store import init_db
from .config import load_conf
from .mail import send_apt
from .geo import match_hood


MIN_LISTINGS = 200
GMAP_TEMPLATE = 'google.com/maps/?q={lat:f},{lng:f}'


def fmt(dct):
    return '%s -- %s' % (dct['title'], dct['url'])


def mk_logger(fname):
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    handler = logging.handlers.TimedRotatingFileHandler(
        fname,
        when='D',
        interval=2,
        backupCount=2
    )
    logger.addHandler(handler)
    handler = logging.StreamHandler()
    logger.addHandler(handler)


def collect_new(scraper, conf, db):
    logger = logging.getLogger()
    new_listings = []
    listings = scraper.collect_listings(MIN_LISTINGS, conf)
    logger.info('Collected %d listings.' % len(listings))
    for listing in listings:
        data_id = listing['data_id']
        if db.query(data_id):
            logger.info('SKIPPING ' + fmt(listing))
            continue

        # logger.info('ADDING ' + fmt(listing))
        new_listings.append(listing)

    logger.info('%d are new.' % len(new_listings))
    return new_listings


def parse(listings, scraper, db):
    logger = logging.getLogger()
    apartments = []
    for i, listing in enumerate(listings):
        url = listing['url']
        data_id = listing['data_id']
        try:
            logger.info('%d ' % i + 'PARSING ' + fmt(listing))
            html = requests.get(url).text
            apt = scraper.parse_posting(html)
        except Exception:
            logger.exception('EXCEPTION IN PARSE')
            continue

        apt['url'] = url
        apt['data_id'] = data_id
        if not apt['images']:
            logger.info('Found no images.')
            db.add(data_id)
            continue
        apartments.append(apt)

    return apartments


def filtr(apartments, conf, db):
    logger = logging.getLogger()
    ret = []
    for i, apt in enumerate(apartments):
        hood = match_hood(apt['geo'], conf['hoods'])
        if hood is False:
            logger.info('%d NOPE' % i)
            db.add(apt['data_id'])
            continue

        logger.info('%d YEP' % i)
        apt['hood'] = hood
        ret.append(apt)

    return ret


def send(apartments, conf, db):
    logger = logging.getLogger()
    for apt in apartments:
        logger.info('SENDING ' + fmt(apt))
        send_apt(
            apt,
            fromaddr=conf['fromaddr'],
            passwd=conf['passwd'],
            toaddr=conf['toaddr'],
            dry=conf.get('dry_run', False),
        )
        db.add(apt['data_id'])


def main(scraper, conf, db):
    listings = collect_new(scraper, conf, db)
    apartments = parse(listings, scraper, db)
    apartments = filtr(apartments, conf, db)
    send(apartments, conf, db)


def cli():
    work_dir = os.path.abspath('.')
    conf = load_conf(work_dir)
    argc = len(sys.argv)
    if argc != 2:
        print('Must have exactly one argument')
        sys.exit(1)
    prog = sys.argv[1]
    if prog == 'cl':
        name = 'craigslist'
        scraper = scrapers.craigslist
    elif prog == 'kj':
        name = 'kijiji'
        scraper = scrapers.kijiji
    else:
        print('Invalid program argument %s' % prog)
        sys.exit(1)

    log_filename = name + '.log'
    db_filename = name + '.db'
    mk_logger(os.path.join(work_dir, log_filename))
    db = init_db(os.path.join(work_dir, db_filename))
    logger = logging.getLogger()
    sep = '-'*50
    msg = sep + '\nSTARTED:  %s\n' % datetime.datetime.now() + sep
    logger.info(msg)
    try:
        main(scraper, conf, db)
    except KeyboardInterrupt:
        logger.info('Aborted!')
        sys.exit(152)
    except:
        logger.exception('EXCEPTION IN MAIN')

    db.close()


if __name__ == '__main__':
    cli()
