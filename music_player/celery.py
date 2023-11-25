from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_player.settings')

app = Celery('Music-Platform')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')


# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

app.conf.broker_url = 'amqp://guest:guest@localhost:5672/'
app.conf.result_backend = 'rpc://'
app.conf.result_expires = timedelta(days=1)
