# So as to not hammer the craigslist/kijiji servers too much, all of the work
# is done synchronously
from .factory import create_celery_app
# from .database import get_jobs


celery = create_celery_app()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, cron.s())


@celery.task
def cron():
    """
    Starts task for each job in the database.
    """
    foo = err
    return 42
    print('!Run!')
    from datetime import datetime
    open('/Users/selimb/Projects/aptscraper/out', 'a').write(datetime.now())
    for job in get_jobs():
        print('Job ' + repr(job))
        run_job.delay(job._id)

