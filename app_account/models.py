from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    is_author = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='profile_image', null=True, blank=True)
    cellphone_no = models.CharField(max_length=14, unique=True, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    vip_due_date = models.DateTimeField(default=timezone.now)
    address = models.ManyToManyField('UserAddress', related_name='addresses', blank=True)
    email_active_code = models.CharField(max_length=100, blank=True, null=True)
    user_cart = models.CharField(max_length=1000, null=True, blank=True)

    def is_vip_due_date(self):
        if self.vip_due_date > timezone.now():
            return True
        else:
            return False

    # instead of showing False/True in admin panel, Tick or Cross shapes will be displayed
    is_vip_due_date.boolean = True
    is_vip_due_date.short_description = 'VIP'


class UserAddress(models.Model):
    full_address = models.CharField(max_length=1000, null=True, blank=True)
