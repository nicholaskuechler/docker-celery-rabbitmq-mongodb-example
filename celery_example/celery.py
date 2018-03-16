from __future__ import absolute_import

from celery import Celery


app = Celery('celery_example',
             broker='amqp://admin:mypass@rabbit:5672',
             backend='rpc://',
             include=['celery_example.tasks'])
