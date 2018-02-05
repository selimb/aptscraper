"""
Insensitive configuration goes here.
"""
# inspired from http://skillachie.com/2013/06/15/intro-celery-and-mongodb/
# and http://flask.pocoo.org/docs/0.12/config/#development-production
import os


APP_NAME = 'DONNA'


def get_env(key):
    return os.environ.get(key, None)


def assert_no_defaults(config):
    def is_caps(name):
        return name.upper() == name
    pairs = [member for member in inspect.getmembers(config) if is_caps(member[0])]
    dct = dict(pairs)
    for key, value in dct.items():
        assert value is not None, 'Unset value for {}'.format(key)


class Config:
    # Flask
    DEBUG = False
    TESTING = False
    SECRET_KEY = get_env('SECRET_KEY')

    # Network
    USE_PROXY = False
    PROXY_HOST = 'proxy-nl.privateinternetaccess.com'
    PROXY_PORT = '1080'
    PROXY_USER = get_env('PROXY_USER')
    PROXY_PASS = get_env('PROXY_PASS')

    # Mail

    # rpyc
    RPYC_HOST = 'localhost'
    RPYC_PORT = 12345

    # Mongo
    MONGO_HOST = get_env('MONGO_HOST')
    MONGO_PORT = get_env('MONGO_PORT')
    MONGO_DB_NAME = APP_NAME
    MONGO_SCHEDULER_COLLECTION = 'scheduler'
    MONGO_JOBS_COLLECTION = 'jobs'


class ProductionConfig(Config):
    USE_PROXY = True


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


def get_config():
    # TODO: Document
    mode = get_env(APP_NAME + '_MODE')
    mode = 'dev' if mode is None else mode.lower()
    if mode == 'dev':
        return DevelopmentConfig
    elif mode == 'test':
        return TestingConfig
    elif mode == 'prod':
        config = ProductionConfig
        assert_no_defaults(config)
    else:
        raise AssertionError("Mode {} is invalid.".format(mode))


CONF = get_config()

