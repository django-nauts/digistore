from django.urls import path
from . import views

app_name = 'app_product'

urlpatterns = [
    path('', views.product_list, name='product_list_page'),
    path('<slug:slug>/', views.product_detail, name='product_detail_page'),
]