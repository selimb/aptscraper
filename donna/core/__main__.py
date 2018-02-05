import logging
import rpyc
from rpyc.utils.server import ThreadedServer


def setup_logger(job_id):
    raise NotImplementedError


def run_job(job_id):
    setup_logger(job_id)
    logger.info('Starting crawl for job: ' + str(job_id))
    job = database.get_job(job_id)
    store = database.get_store(job)
    logger = logging.get_logger(__name__)
    for base_url in job.queries:
        crawler.crawl(base_url, job.hoods, job.to_email, store)


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
    db_client = create_client()
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
