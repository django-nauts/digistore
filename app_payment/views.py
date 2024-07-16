from django.shortcuts import render
from django.views import View

from app_cart.cart import Cart

from app_payment.models import ShippingAddress


# Create your views here.

def checkout(request):
    selected_shipping_address = ShippingAddress.objects.filter(user_id=request.user.id, main_address=True).first()
    cart = Cart(request)
    context = {
        'cart': cart,
        'selected_shipping_address':selected_shipping_address
    }
    return render(request, 'app_payment/checkout.html', context)
