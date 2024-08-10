from django.contrib import admin

from .models import Product, Category, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

