import logging
import sys
import time
import uuid

from celery_example.tasks import demo_celery_task
from celery_example.tasks import fetch_url


logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


if __name__ == '__main__':
    # Demo 1: Fetch a url and store results in mongodb
    url = "http://nicholaskuechler.com/"
    fetch_url_result = fetch_url.delay(url)
    logging.info("fetch_url_result: %s" % (fetch_url_result))

    # Demo 2: Send randomized data to celery workers every few seconds
    while True:
        work_id = str(uuid.uuid4())
        logging.info("Sending work_id: %s" % (work_id))

        result = demo_celery_task.delay(work_id)
        logging.info("work_id result: %s" % (result))

        logging.info("sleeping for 10 seconds...")
        time.sleep(10)
