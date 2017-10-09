# inspired from http://skillachie.com/2013/06/15/intro-celery-and-mongodb/
_host = '127.0.0.1'
_port = 27017
_database = 'jobs'
BROKER_URL = 'mongodb://{host}:{port}/{database}'.format(
    host=_host,
    port=_port,
    database=_database
)
CELERY_RESULT_BACKEND = 'mongodb'
CELERY_MONGODB_BACKEND_SETTINGS = {
    'host': _host,
    'port': _port,
    'database': _database,
}
