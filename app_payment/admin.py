from django.contrib import admin
from .models import ShippingAddress, OrderItem, Order


# Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'is_author', 'is_vip_due_date', 'is_superuser', 'is_staff', 'is_active']
#     # list_filter = ['']
#     # search_fields = [']
#     # raw_id_fields = ['']
#     # date_hierarchy = ''
#     # ordering = ['']

class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ('product',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'date_ordered', 'is_paid')
	list_filter = ('is_paid',)
	inlines = (OrderItemInline,)


admin.site.register(ShippingAddress)