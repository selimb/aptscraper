from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient

from ..config import CONF


def create_db():
    client = MongoClient(conf.MONGO_HOST, conf.MONGO_PORT)
    return client[conf.MONGO_DB]


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

