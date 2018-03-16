from __future__ import absolute_import

import logging
import requests
import sys
import time

from pymongo import MongoClient

from celery_example.celery import app


logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


# For storing celery worker results in MongoDB
client = MongoClient('mongo', 27017)
db = client.mongodb_test
collection = db.celery_test
post = db.test


@app.task(bind=True, default_retry_delay=10)
def fetch_url(self, url):
    print("fetch_url is working on: %s" % (url))
    try:
        r = requests.get(url)
        post.insert({"status": r.status_code,
                     "creat_time": time.time()})
        print("fetch_url: Successfully fetched url: %s" % (url))
    except Exception as exc:
        logging.exception("fetch_url hit an error: %s" % (exc))
        raise self.retry(exc=exc)
    return r.status_code


@app.task(bind=True, default_retry_delay=10)
def demo_celery_task(self, i):
    print("demo_celery_task is working on: %s" % (i))
