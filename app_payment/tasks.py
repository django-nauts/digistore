from celery import shared_task
from app_payment.models import Order


@shared_task
def remove_unpaid_orders():
    print('Removing unpaid orders...')
    qs = Order.objects.filter(is_paid=False)
    qs.delete()
    print('Is done!')

