from django.urls import path
from . import views

app_name = 'app_dashboard'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard_page'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password_page'),
    path('change-info/', views.ChangeUserInfoView.as_view(), name='change_info_page'),
    path('shipping-address/', views.ShippingAddressView.as_view(), name='shipping_address_page'),
]