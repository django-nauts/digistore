from django.db import models

# Create your models here.

from django.db import models

from app_account.models import User
from app_product.models import Product


# Create your models here.


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=300)
    email = models.EmailField()
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    main_address = models.BooleanField(default=True)


class Order(models.Model):
    full_name = models.CharField(max_length=300)
    email = models.EmailField()
    shipping_address = models.TextField(max_length=500)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {str(self.id)}'

    def get_total_price(self):
        # "items" is related name in the OrderItem Model
        total = sum(item.get_cost() for item in self.items.all())
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.qty
