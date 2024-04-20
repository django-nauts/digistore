from django.shortcuts import render

# Create your views here.


def cart(request):
    return render(request, 'app_cart/cart.html')


def whishlist(request):
    return render(request, 'app_cart/whishlist.html')