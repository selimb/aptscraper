from pymongo import MongoClient

from ..config import CONF
from . import database


def init_all():
    """
    Initialize everything.
    """
    client = create_client()
    database.init_db(client)
    # create scheduler


def create_client():
    return MongoClient(CONF.MONGO_HOST, int(CONF.MONGO_PORT))


def create_scheduler():
    from apscheduler.schedulers.background import BackgroundScheduler
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

