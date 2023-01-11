
from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.store, name='store'),

    path('search/<slug:category_slug>', views.list_categories, name='list-category'),

    path('product/<slug:product_slug>', views.product_info, name='product-info'),
    
]
