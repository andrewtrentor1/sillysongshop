"""
Celery configuration for weirdsongfactory project.
https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
"""
import os

from celery import Celery

from django.conf import settings

# Set the default Django settings module for the 'celery' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weirdsongfactory.settings')

app = Celery("weirdsongfactory")

# Configure Celery to use 'solo' pool on Windows
if os.name == 'nt':
    app.conf.update(
        broker_connection_retry_on_startup=True,
        worker_pool='solo',
    )

# Read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover and load tasks.py from all registered Django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
