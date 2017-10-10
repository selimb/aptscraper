"""
Insensitive configuration goes here.
"""
# inspired from http://skillachie.com/2013/06/15/intro-celery-and-mongodb/
# and http://flask.pocoo.org/docs/0.12/config/#development-production
import os


APP_NAME = 'DONNA'
_celery_db = 'celery_tasks'
defaults = {
    'SECRET_KEY': 'secret-key',
    'MODE': 'dev',
}


def getenv(var):
    default = defaults.get(var, None)
    return os.environ.get('_'.join([APP_NAME, var]), default)


class Config:
    # Flask
    DEBUG = False
    TESTING = False
    SECRET_KEY = getenv('SECRET_KEY')

    # Network
    USE_PROXY = False
    PROXY_HOST = 'proxy-nl.privateinternetaccess.com'
    PROXY_PORT = '1080'
    PROXY_USER = getenv('PROXY_USER')
    PROXY_PASS = getenv('PROXY_PASS')

    # Mail

    # rpyc
    RPYC_HOST = 'localhost'
    RPYC_PORT = 12345

    # Mongo
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017

    # Scheduler
    SCHEDULER_MONGO_COLLECTION = 'jobs'


class ProductionConfig(Config):
    MONGO_DB = 'prod'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


def get_config():
    # TODO: Document
    mode = getenv('MODE').lower()
    if mode == 'dev':
        return DevelopmentConfig
    elif mode == 'test':
        return TestingConfig
    elif mode == 'prod':
        config = ProductionConfig
        # TODO
    else:
        raise AssertionError("Mode {} is invalid.".format(mode))


CONF = get_config()
