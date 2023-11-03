import os
from celery import Celery
from celery.beat import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    "get_student_with_interval": {
        "task": "apps.initialization.tasks.get_student_data",
        "schedule": crontab(minute=0, hour='*/2,*/3')
        # Execute every even hour, and every hour divisible by three.
        # This means: at every hour except: 1am, 5am, 7am, 11am, 1pm, 5pm, 7pm, 11pm
    }
}

app.autodiscover_tasks()