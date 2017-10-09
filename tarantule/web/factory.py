from celery import Celery


def create_celery_app():
    app = Celery()
    app.config_from_object('tarantule.web.celeryconfig')
    return app
