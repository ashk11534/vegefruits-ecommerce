from django.shortcuts import render, get_object_or_404

from .cart import Cart

from store.models import Product

from django.http import JsonResponse

# Create your views here.

def cart_summary(request):

    return render(request, 'cart/cart-summary.html')


def cart_add(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))

        quantity = int(request.POST.get('quantity'))

        product = get_object_or_404(Product, id = product_id)

        cart.add(product=product, qty=quantity)

        cart_quantity = len(cart)

        response = JsonResponse({'qty': cart_quantity})

        return response


def cart_delete(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = request.POST.get('product_id') 

        cart.delete(product_id=product_id)

        cart_quantity = len(cart)

        cart_total = cart.get_total_price()

        response = JsonResponse({'qty': cart_quantity, 'cart_total': cart_total})

        return response