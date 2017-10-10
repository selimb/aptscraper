from apscheduler.schedulers.background import BackgroundScheduler

from donna.config import CONF
# from .database import get_jobs


def create_scheduler():
    print('Creating scheduler')
    scheduler = BackgroundScheduler()
    mongo_client_kwargs = dict(
        host=CONF.MONGO_HOST,
        port=CONF.MONGO_PORT,
    )
    scheduler.add_jobstore(
        'mongodb',
        collection=CONF.SCHEDULER_MONGO_COLLECTION,
        **mongo_client_kwargs
    )
    return scheduler

