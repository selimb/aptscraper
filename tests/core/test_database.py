import pytest

from donna.core import database


def test_add_job_get_jobs(db):
    kwargs = dict(queries=["google.ca"], hoods=None, to_email="me@hello.com")
    job = database.Job(**kwargs)
    job_id = database.add_job(job)

    assert job == database.get_jobs([job_id])[0]

    kwargs['to_email'] = 'him@bye.com'
    job2 = database.Job(**kwargs)
    job_id2 = database.add_job(job2)

    jobs = database.get_jobs([job_id, job_id2])
    for job in [job, job2]:
        assert job in jobs


def test_scrape_history(db):
    job_ids = []
    for to_email in ["me@hello.com", "him@bye.ca"]:
        job = database.Job(queries=["duckduckgo.com"], hoods=None, to_email=to_email)
        job_ids.append(database.add_job(job))

    history = database.ScrapeHistory(job_ids[0])
    urls = ["duckduckgo.com/%i" % i for i in range(2)]
    history.mark_visited(urls)

    assert history.was_visited(urls) == [True]*2

    history = database.ScrapeHistory(job_ids[1])
    assert history.was_visited(urls) == [False]*2
    history.mark_visited([urls[1]])
    assert [False, True] == history.was_visited(urls)

