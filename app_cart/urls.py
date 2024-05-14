from django.urls import path
from . import views

app_name = 'app_cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail_page'),
    path('add/', views.cart_add, name='cart_add'),
    path('delete/', views.cart_delete, name='cart_delete'),
    path('update/', views.cart_update, name='cart_update'),
    path('whishlist/', views.whishlist, name='whishlist_page'),
]