from bson.objectid import ObjectId


_DB = None


def get_db():
    assert _DB is not None
    return _DB


def init_db(client):
    global _DB
    _DB = client.donna


class Job:
    def __init__(self, queries, hoods, to_email):
        self.queries = queries
        self.hoods = hoods
        self.to_email = to_email

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ScrapeHistory:
    def __init__(self, job_id):
        self.job_id = ObjectId(job_id)

    def mark_visited(self, urls):
        documents = [
            {"job_id": self.job_id, "url": url}
            for url in urls
        ]
        _history().insert_many(documents)

    def was_visited(self, urls):
        # TODO: Only need to see if it's there.
        # Projection to None?
        # Batch retrieve?
        docs = _history().find(
            {"job_id": self.job_id, "url": {"$in": urls}},
            projection={"url": True, "_id": False}
        )
        visited = set(doc["url"] for doc in docs)
        return [url in visited for url in urls]


def add_job(job):
    document = {
        'queries': job.queries,
        'hoods': job.hoods,
        'to_email': job.to_email
    }
    inserted = _jobs().insert_one(document)
    return inserted.inserted_id


def get_jobs(job_ids):
    # TODO: Could also use .find({"_id": {"$in": ids}})
    # Don't know if returning in order is important
    job_ids = map(ObjectId, job_ids)
    return [
        _job_from_document(_jobs().find_one({"_id": job_id}))
        for job_id in job_ids
    ]


def edit_job(job_id, job):
    raise NotImplementedError


def _job_from_document(document):
    document.pop("_id")
    return Job(**document)


def _jobs():
    return get_db()["jobs"]


def _history():
    return get_db()["history"]

