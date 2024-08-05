from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from app_cart.cart import Cart
from app_payment.forms import OrderCreateForm

from app_payment.models import ShippingAddress, OrderItem, Order
import stripe

from config import settings

# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def checkout(request):
    selected_shipping_address = ShippingAddress.objects.filter(user_id=request.user.id, main_address=True).first()
    cart = Cart(request)
    shipping_address = (selected_shipping_address.city + ', ' + selected_shipping_address.state + ', '
                        + selected_shipping_address.address + ', ' + selected_shipping_address.zipcode)
    order = Order.objects.create(user=request.user,
                                 full_name=selected_shipping_address.full_name,
                                 email=selected_shipping_address.email,
                                 shipping_address=shipping_address,
                                 amount_paid=cart.get_total_price())
    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], qty=item['qty'], price=item['price'])
    context = {
        'cart': cart,
        'selected_shipping_address': selected_shipping_address,
        'order': order,
    }
    return render(request, 'app_payment/checkout.html', context)


def payment_process(request, order_id):
    order = Order.objects.get(id=order_id)
    # Creating a new session with name "order_pay" to save id of order in it
    request.session['order_pay'] = {'order_id': order.id, }
    print(order)

    success_url = request.build_absolute_uri(reverse('app_payment:completed_page'))
    cancel_url = request.build_absolute_uri(reverse('app_payment:canceled_page'))
    # Stripe checkout session data
    session_data = {
        'mode': 'payment',
        'client_reference_id': order.id,
        'success_url': success_url,
        'cancel_url': cancel_url,
        'line_items': []
    }
    # add order items to the Stripe checkout session
    # "items" is related name in the OrderItem Model
    for item in order.items.all():
        session_data['line_items'].append({
            'price_data': {
                'unit_amount': int(item.price * Decimal('100')),
                'currency': 'usd',
                'product_data': {
                    'name': item.product.title,
                },
            },
            'quantity': item.qty,
        })
    # create Stripe checkout session
    session = stripe.checkout.Session.create(**session_data)
    # redirect to Stripe payment form
    return redirect(session.url, code=303)


def payment_completed(request):
    if request.session['order_pay'] and request.session['session_key']:
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=order_id)
        order.is_paid = True
        order.save()
        # Delete sessions to empty out the cart and order_id
        del request.session['session_key']
        del request.session['order_pay']
        return render(request, 'app_payment/completed.html')
    else:
        return render(request, '404.html')


def payment_canceled(request):
    return render(request, 'app_payment/canceled.html')
