from collections import namedtuple

from .factory import create_db

db = create_db()


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


def get_jobs(user_id=None):
    jobs_collection = db.jobs
    filtr = {'user_id': user_id} if user_id else None
    print('Get Jobs')
    for job_dict in jobs_collection.find(filtr):
        print(repr(job_dict))
        yield Job(**job_dict)

