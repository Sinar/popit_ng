import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', "popit_ng.settings")

from django.conf import settings

app = Celery('popit')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))