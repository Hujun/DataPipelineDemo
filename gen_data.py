#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import random
import os

from celery import Celery
from celery.schedules import crontab
import redis

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_URL = 'redis://{}:{}/{}'.format(REDIS_HOST, REDIS_PORT, REDIS_DB)
PUB_CHANNEL_NAME = 'data_pipeline_demo'

app = Celery()
app.conf.broker_url = REDIS_URL
app.conf.result_backend = REDIS_URL
app.conf.beat_schedule = {
    'random-float-every-2-seconds': {
        'task': 'gen_data.random_float',
        'schedule': 2.0,
    }
}

# init global redis connection for publish
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

@app.task(bind=True)
def random_float(self):
    """publish random float in redis channel
    """
    data = '{},{}'.format(datetime.now(), random.uniform(0.0, 100.0))
    r.publish(PUB_CHANNEL_NAME, data)
    print('data sent: {}'.format(data))
