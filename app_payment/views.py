from django.shortcuts import render
from django.views import View

from app_cart.cart import Cart


# Create your views here.

def checkout(request):
    cart = Cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'app_payment/checkout.html', context)

