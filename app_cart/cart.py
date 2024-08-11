from decimal import Decimal

from app_account.models import User
from app_product.models import Product


# ******************************* NOTES (FYI) **********************************************
# Items in our session dictionary:
# >>> from django.contrib.sessions.models import Session
# >>> skey=Session.objects.get(pk="g63naqzrny1qub8oasvfu9pjdtz7wsa6")
# >>> skey.get_decoded()
# {'session_key': {'1': {'price': '10.54', 'qty': 1}, '2': {'price': '5.68', 'qty': 3}}}

# WITHOUT Cart persistence:
# 1) If we are logged and add some items in our cart, if we don't write codes for cart persistence after
# logging out the cart will be empty therefore we have to use cart persistence
# 2) if we weren't logged in, and we add some items in our cart, after logging in the items
# will be in out cart but after logged out will disappear again

# WITH Cart persistence:
# You are able to login with any device and access to your specific cart
# ********************************************************************************************


class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add_to_cart(self, product, qty):
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] += qty
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': int(qty)}
        self.save_modification()

        # Adding persistence to our cart after logged out the items will remain inside of specific user cart
        if self.request.user.is_authenticated:
            current_user = User.objects.filter(id=self.request.user.id)
            user_cart = str(self.cart)
            user_cart = user_cart.replace("\'", "\"")
            current_user.update(user_cart=user_cart)

    def db_add(self, product_id, qty, price):
        product_id = str(product_id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] += qty
        else:
            self.cart[product_id] = {'price': str(price), 'qty': int(qty)}
        self.save_modification()

        # Adding persistence to our catt after logged out the items will remain inside of specific user cart
        if self.request.user.is_authenticated:
            current_user = User.objects.filter(id=self.request.user.id)
            user_cart = str(self.cart)
            user_cart = user_cart.replace("\'", "\"")
            current_user.update(user_cart=user_cart)

    # delete item from cart/basket one by one
    def delete_from_cart(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save_modification()

        # Adding persistence to our catt after logged out the items will remain inside of specific user cart
        if self.request.user.is_authenticated:
            current_user = User.objects.filter(id=self.request.user.id)
            user_cart = str(self.cart)
            user_cart = user_cart.replace("\'", "\"")
            current_user.update(user_cart=user_cart)

    def update_cart(self, product_id, product_qty):
        cart = self.cart
        product_id = str(product_id)
        product_qty = int(product_qty)
        cart[product_id]['qty'] = product_qty
        self.save_modification()

        # Adding persistence to our catt after logged out the items will remain inside of specific user cart
        if self.request.user.is_authenticated:
            current_user = User.objects.filter(id=self.request.user.id)
            user_cart = str(self.cart)
            user_cart = user_cart.replace("\'", "\"")
            current_user.update(user_cart=user_cart)

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            # cart example ~> {"1": {"price": "10.54", "qty": 4}, "2": {"price": "5.68", "qty": 5}}
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    # subtotal of cart
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    def save_modification(self):
        self.session.modified = True
