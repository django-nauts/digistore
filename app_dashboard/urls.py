from django.urls import path
from . import views

app_name = 'app_dashboard'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard_page'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password_page'),
    path('change-info/', views.ChangeUserInfoView.as_view(), name='change_info_page'),
    path('shipping-address/', views.ShippingAddressView.as_view(), name='shipping_address_page'),
    path('shipping-address/delete/', views.shipping_address_delete, name='shipping_address_delete'),
    path('shipping-address/chosen/', views.chosen_shipping_address, name='shipping_address_chosen_page'),
    path('shipping-address/check/', views.check_shipping_address, name='shipping_address_check'),
    path('orders/', views.Orders.as_view(), name='orders_page'),
    path('orders/<int:order_id>/', views.OrderDetail.as_view(), name='order_detail_page'),
]
