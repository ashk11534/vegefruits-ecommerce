from django.shortcuts import render, get_object_or_404, redirect

from .models import Product, Category

# Create your views here.

def store(request):

    products = Product.objects.all()

    context = {'products': products}

    return render(request, 'store/store.html', context=context)

def categories(request):

    all_categories = Category.objects.all()

    return {'all_categories': all_categories}

def list_categories(request, category_slug):

    category = get_object_or_404(Category, slug=category_slug)

    category_products = Product.objects.filter(category=category)

    context = {'category': category, 'category_products': category_products}

    return render(request, 'store/list-category.html', context=context)

def product_info(request, product_slug):

    product = get_object_or_404(Product, slug=product_slug)

    context = {'product': product}

    return render(request, 'store/product-info.html', context=context)