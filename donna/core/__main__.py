import rpyc
from rpyc.utils.server import ThreadedServer

from .scheduler import create_scheduler

def main():
    print('!Run!')


def run_job(job_id):
    print('Running job ' + job_id)
    # Setup logging
    # Setup DB
    # Setup spiders
    # Spider requires:
# 1. Start from base url
# 2. S
# 1. Collect listings -- requires network
# 2. Filter listings -- reuires db
# 3. Scrape ads
    # Run all

# collect listings -- REQUESTS, LOG
#   while:
#       html = get(base_url)  # REQUESTS
#       soup = parse(html)
#       scrape_listings(soup)
#       url = join(base_url, get_next_page(soup))
#       html = get(base_url)  # REQUESTS
#       soup = parse(html)
#       scrape_listings(soup)

# process listings -- DB, LOG
    # new_listings = filter_listings(listings)  # DB GET

# collect ad_htmls -- REQUESTS, LOG
#   urls = (join(base_url, listing) for listing in new_listings)
#   htmls = map(get, urls)  # REQUESTS

# scrape ads
#   ads = map(scrape_ad, html)
#   add_ads_to_db(ads)  # DB PUT
#   filter_ads(ads)  # GEO, etc...
#   mail_ads(ads)  # MAIL

#   spiders = setup_spiders(queries, hoods)
#   for base_url in queries:

def square(number):
    print(number*number)
    return number*number


def setup_donna(scheduler):
    class DonnaService(rpyc.Service):
        def exposed_add_job(self, number):
            return scheduler.add_job(square, 'interval', args=[number], seconds=5)

        def exposed_get_jobs(self,):
            return [job.id for job in scheduler.get_jobs()]

        def exposed_remove_job(self, job_id):
            scheduler.remove_job(job_id)

        def exposed_say_hello(self):
            return 'hello'

    return DonnaService


if __name__ == '__main__':
    scheduler = create_scheduler()
    scheduler.start()
    service_cls = setup_donna(scheduler)
    server = ThreadedServer(service_cls, port=12345)
    try:
        server.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()
