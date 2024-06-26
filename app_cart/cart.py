from decimal import Decimal

from app_product.models import Product


# Items in our session dectionary:
# >>> from django.contrib.sessions.models import Session
# >>> skey=Session.objects.get(pk="g63naqzrny1qub8oasvfu9pjdtz7wsa6")
# >>> skey.get_decoded()
# {'session_key': {'1': {'price': '10.54', 'qty': 1}, '2': {'price': '5.68', 'qty': 3}}}


class Cart():
    def __init__(self, request):
        self.session = request.session
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



    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    # delete item from cart/basket one by one
    def delete_from_cart(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save_modification()

    def update_cart(self, product_id, product_qty):
        cart = self.cart
        product_id = str(product_id)
        product_qty = int(product_qty)
        cart[product_id]['qty'] = product_qty
        self.save_modification()

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

        # subtotal of cart

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    # def unit_total_price(self, product_id, product_qty):
    #     cart = self.cart.copy()
    #     product_id = str(product_id)
    #     product_qty = int(product_qty)
    #     price = Decimal(cart[product_id]['price'])
    #     print("+++++++++++++++++++++++++++++++++++")
    #     print(price)
    #     print("+++++++++++++++++++++++++++++++++++")
    #     cart[product_id]['total_price'] = product_qty * price
    #     unit_total_price = cart[product_id]['total_price']
    #     self.save_modification()
    #     return unit_total_price

    def save_modification(self):
        self.session.modified = True
