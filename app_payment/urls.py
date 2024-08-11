from django.urls import path
from . import views, webhooks

app_name = 'app_payment'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout_page'),
    path('process/<int:order_id>/', views.payment_process, name='process_page'),
    path('completed/', views.payment_completed, name='completed_page'),
    path('canceled/', views.payment_canceled, name='canceled_page'),
    # path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'), # Doesnt work for Ventuno so I comment it
]
