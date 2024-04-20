from django.urls import path
from . import views

app_name = 'app_cart'

urlpatterns = [
    path('', views.cart, name='cart_page'),
    path('whishlist/', views.whishlist, name='whishlist_page'),

]