
from store.models import Product

from decimal import Decimal

class Cart():

    def __init__(self, request):
        
        self.session = request.session

        cart = self.session.get('session_key')

        if 'session_key' not in self.session:

            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, qty):

        product_id = str(product.id)

        if product_id in self.cart:

            self.cart[product_id]['qty'] = qty

        else:

            self.cart[product_id] = {'price': str(product.price), 'qty': qty}

        self.session.modified = True


    def delete(self, product_id):

        if product_id in self.cart:

            del self.cart[product_id]

        self.session.modified = True


    def __iter__(self):

        all_product_ids = self.cart.keys()

        products = Product.objects.filter(id__in = all_product_ids)

        cart = self.cart.copy()

        for product in products:

            cart[str(product.id)]['product'] = product

        for item in cart.values():

            item['price'] = Decimal(item['price'])

            item['total'] = item['price'] * item['qty']

            yield item


    def __len__(self):

        return sum(item['qty'] for item in self.cart.values())

    
    def get_total_price(self):

        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())