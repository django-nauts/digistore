from django.contrib import admin
from .models import User

# Register your models here.




class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_author', 'is_vip_due_date', 'is_superuser', 'is_staff', 'is_active']
    # list_filter = ['']
    # search_fields = [']
    # raw_id_fields = ['']
    # date_hierarchy = ''
    # ordering = ['']

admin.site.register(User, UserAdmin)
