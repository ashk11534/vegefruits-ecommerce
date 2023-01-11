from django.shortcuts import render, redirect

from .models import ShippingAddress, Order, OrderItem

from cart.cart import Cart

from django.contrib.sites.shortcuts import get_current_site

import stripe

# Create your views here.

def checkout(request):

    if request.user.is_authenticated:

        try:

            shipping_address = ShippingAddress.objects.get(user = request.user)

            context = {'shipping': shipping_address}

            return render(request, 'payment/checkout.html', context = context)

        except ShippingAddress.DoesNotExist:

            return render(request, 'payment/checkout.html')

    else:

        return render(request, 'payment/checkout.html')


def complete_order(request):

    if request.method == 'POST':

        name = request.POST.get('name')

        email = request.POST.get('email')

        address1 = request.POST.get('address1')

        address2 = request.POST.get('address2')

        city = request.POST.get('city')

        zipcode = request.POST.get('zipcode')

        shipping_address = (address1 + '\n' + address2 + '\n' + city + '\n' + zipcode)

        cart = Cart(request)

        total_cost = cart.get_total_price()

        if request.user.is_authenticated:

            order = Order.objects.create(full_name = name, email = email, shipping_address = shipping_address, amount_paid = total_cost, user = request.user)

            for item in cart:

                OrderItem.objects.create(order = order, product = item['product'], quantity = item['qty'], price = item['total'], user = request.user)
            
        else:
            order = Order.objects.create(full_name = name, email = email, shipping_address = shipping_address, amount_paid = total_cost)

            for item in cart:

                OrderItem.objects.create(order = order, product = item['product'], quantity = item['qty'], price = item['total'])

        return redirect('create-checkout-session', order_id = order.id)


def payment_success(request):

    for key in list(request.session.keys()):

        if key == 'session_key':

            del request.session[key]

    return render(request, 'payment/payment-success.html')


def payment_failed(request):

    return render(request, 'payment/payment-failed.html')
            

stripe.api_key = 'sk_test_51MM7w3Ht1mwBhPGTXQokC1brW0iXcODxBqyRRjKgXyBCvQ0xEs6x1468LGQAkNk38phh9quqKzgWtbmKh8MFqfqS00L4EoLOzZ'

def create_checkout_session(request, order_id):

    current_site = get_current_site(request)

    try:

        order = Order.objects.get(pk = order_id)

    except Order.DoesNotExist:

        order = 'Unknown'

    session = stripe.checkout.Session.create(

        line_items=[{

        'price_data': {

            'currency': 'BDT',

            'product_data': {

            'name': order,

            },

            'unit_amount': int(order.amount_paid) * 100,

        },

        'quantity': 1,

        }],

        mode='payment',

        success_url = f'http://{current_site}/payment/payment-success',
        
        cancel_url = f'http://{current_site}/payment/payment-failed',
    )

    return redirect(session.url, code=303)
