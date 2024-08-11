from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .cart import Cart
from app_product.models import Product
from app_payment.models import ShippingAddress


# Create your views here.

# Show detail of cart
def cart_detail(request):
    selected_shipping_address = ShippingAddress.objects.filter(user_id = request.user.id, main_address= True).first()
    cart = Cart(request)
    context = {
        'cart': cart,
        'selected_shipping_address':selected_shipping_address,
    }
    return render(request, 'app_cart/cart.html', context)


# Add item to your basket/cart from product page
def cart_add(request):
    cart = Cart(request)
    product_id = int(request.POST.get('productId'))
    product_qty = int(request.POST.get('productQty'))
    product = get_object_or_404(Product, id=product_id)
    cart.add_to_cart(product=product, qty=product_qty)
    cart_qty = cart.__len__()
    return JsonResponse({'qty': cart_qty})


# Delete one row in the cart
def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('productId')
        cart.delete_from_cart(product_id=product_id)
        cart_qty = cart.__len__()
        subtotal = cart.get_total_price()
        return JsonResponse({'success': True, 'subtotal': subtotal, 'qty': cart_qty})


# Update qty of each row in cart (Increment & Decrement)
def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('productId')
        product_qty = request.POST.get('productQty')
        product = Product.objects.get(id=int(product_id))
        unit_price = product.price
        cart.update_cart(product_id=product_id, product_qty=product_qty)
        cart_qty = cart.__len__()
        subtotal = cart.get_total_price()
        return JsonResponse({'success': 'OK', 'subtotal': subtotal, 'qty': cart_qty, 'unit_price': unit_price})


def whishlist(request):
    return render(request, 'app_cart/whishlist.html')
