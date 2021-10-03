import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6379/1'
app = Celery('social_network', broker=BROKER_URL, backend=BACKEND_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'delete_used_phone_tokens': {
        'task': 'users.tasks.delete_used_phone_tokens_task',
        'schedule': crontab(minute=0, hour='*/3'),
        'args': (),
    }
}
