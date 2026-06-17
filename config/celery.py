import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('bookstore')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-expiring-rentals': {
        'task': 'books.tasks.check_expiring_rentals',
        'schedule': crontab(hour=9, minute=0),  # каждый день в 9:00
    },
    'update-expired-orders': {
        'task': 'books.tasks.update_expired_orders',
        'schedule': crontab(hour=0, minute=0),  # каждый день в полночь
    },
}