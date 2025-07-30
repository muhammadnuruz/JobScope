from django.shortcuts import render
from django.http import JsonResponse

from apps.catalog.api import APIClient
from bot.dispatcher import Config

client = APIClient()

def category_list(request):
    categories = client.get_categories()
    return render(request, 'category_list.html', {'categories': categories})

def product_list(request, category_id):
    products = client.get_products(category_id, page=1)
    return render(request, 'product_list.html', {
        'products': products,
        'category_id': category_id,
        'config_url': Config.URL
    })

def load_more_products(request, category_id, page):
    products = client.get_products(category_id, page=page)
    return JsonResponse({'products': products})
