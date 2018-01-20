from collections import namedtuple

from . import config
from .factory import get_db()


class User:
    def __init__(self, _id, email):
        self._id = _id
        self.email = email


class Job:
    def __init__(self, _id, queries, hoods, to_email):
        self._id = _id
        self.queries = queries
        self.hoods = hoods
        self.to_email = to_email


class ListingStore:
    def __init__(self, collection):
        self._collection = collection

    def mark_checked(self, listings):
        pass

    def was_checked(self, listings):
        pass


def add_job(job):
# TODO test
    document = job.__dict__.pop('_id')
    _get_job_collection().insert_one(job)


def get_jobs(user_id=None):
# TODO test
    filtr = {'user_id': user_id} if user_id else None
    for job_dict in _get_job_collection().find(filtr):
        yield Job(**job_dict)


def _get_job_collection():
    return db[CONF.MONGO_JOBS_COLLECTION]
