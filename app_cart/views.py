from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .cart import Cart
from app_product.models import Product


# Create your views here.


def cart_detail(request):
    return render(request, 'app_cart/cart.html')

# Add item to your basket/cart
def cart_add(request):
    cart = Cart(request)
    product_id = int(request.POST.get('productId'))
    product_qty = int(request.POST.get('productQty'))
    product = get_object_or_404(Product, id=product_id)
    cart.add_to_cart(product=product, qty=product_qty)
    cart_qty=cart.__len__()
    response = JsonResponse({'qty': cart_qty})
    return response


def cart_update(request):
    pass


def cart_delete(request):
    pass


def whishlist(request):
    return render(request, 'app_cart/whishlist.html')
