"""
Provide helper functions for creating global applications.
"""
import os

from celery import Celery
from pymongo import MongoClient

from . import conf


def create_celery_app():
    celery = Celery('EOD_TASKS')
    celery.config_from_object('tarantule.web.config')
    return celery


def create_db():
    client = MongoClient(conf.MONGO_HOST, conf.MONGO_PORT)
    return client[conf.MONGO_DB]

