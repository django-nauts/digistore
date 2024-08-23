import os
from datetime import timedelta

from celery import Celery
from kombu import Exchange, Queue
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'remove_unpaid_orders': {
        'task': 'app_payment.tasks.remove_unpaid_orders',
        'schedule': crontab(minute='*/2', hour='*', day_of_month='*', day_of_week='*', month_of_year='*'),
    }}




# app.conf.task_queues = [
#     Queue('tasks', Exchange('tasks'), routing_key='tasks',
#           queue_arguments={'x-max-priority': 10}),
# ]
#


# app.conf.broker_url = 'amqp://user:**@rabbitmq:5672//'
# app.conf.result_backend = 'rpc://'
# app.conf.task_acks_late = True
# app.conf.task_default_priority = 5
# app.conf.worker_prefetch_multiplier = 1
# app.conf.worker_concurrency = 1
