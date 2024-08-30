from django.core.management.base import BaseCommand
from app_payment.models import Order


class Command(BaseCommand):
    help = 'Remove unpaid orders from database'

    def handle(self, *args, **options):
        qs = Order.objects.filter(is_paid=False)
        qs.delete()
        self.stdout.write('All unpaid orders are removed')