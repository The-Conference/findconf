import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Conferences.settings')

app = Celery('Conferences')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'running_parsers': {
        'task': 'Conference_data.tasks.parser10',
        'schedule': crontab(minute=0, hour=11, day_of_week='thu'),
    },
}
