from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .cart import Cart
from app_product.models import Product


# Create your views here.


def cart_detail(request):
    cart = Cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'app_cart/cart.html', context)


# Add item to your basket/cart
def cart_add(request):
    cart = Cart(request)
    product_id = int(request.POST.get('productId'))
    product_qty = int(request.POST.get('productQty'))
    product = get_object_or_404(Product, id=product_id)
    cart.add_to_cart(product=product, qty=product_qty)
    cart_qty = cart.__len__()
    return JsonResponse({'qty': cart_qty})


def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('productId')
        cart.delete_from_cart(product_id=product_id)
        cart_qty = cart.__len__()
        subtotal = cart.get_total_price()
        return JsonResponse({'success': True, 'subtotal': subtotal, 'qty': cart_qty})


def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('productId')
        product_qty = request.POST.get('productQty')
        cart.update_cart(product_id=product_id, product_qty=product_qty)
        cart_qty = cart.__len__()
        subtotal = cart.get_total_price()

        # unit_total_price = cart.unit_total_price(product_id=product_id, product_qty=product_qty)
        # print("========================================")
        # print(unit_total_price)
        # print("========================================")

        return JsonResponse({'success': 'OK', 'subtotal': subtotal, 'qty': cart_qty, })


def whishlist(request):
    return render(request, 'app_cart/whishlist.html')
