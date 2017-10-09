# So as to not hammer the craigslist/kijiji servers too much, all of the work
# is done synchronously
from .factory import create_celery_app
from .database import get_users
from .spider import setup_spiders


celery = create_celery_app()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, run_all.s())


@celery.task
def run_all():
    """
    Gather all users and start individual tasks.
    """
    print('!Run!')
    all_task_args = []
    for user in get_users():
        all_task_args.append(user['queries'], user['hoods'], user['to_email'])

    for task_args in all_task_args:
        run_spider.delay(*task_args)


@celery.task
def run_spider(queries, hoods, to_email):
    # Setup logging
    # Setup DB
    # Setup spiders
    # Run all
    spiders = setup_spiders(queries, hoods)
    for base_url in queries:

    msg = 'Running spider with:\n%s' % locals()
    print(msg)
