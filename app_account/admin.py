from django.contrib import admin

from app_payment.models import ShippingAddress
from .models import User

# Register your models here.

class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 1


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_author', 'is_vip_due_date', 'is_superuser', 'is_staff', 'is_active']
    inlines = (ShippingAddressInline,)
    # list_filter = ['']
    # search_fields = [']
    # raw_id_fields = ['']
    # date_hierarchy = ''
    # ordering = ['']


admin.site.register(User, UserAdmin)
