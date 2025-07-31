from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound

from apps.catalog.api import APIClient
from bot.dispatcher import Config

client = APIClient()


def category_list(request):
    categories = client.get_categories()
    return render(request, 'category_list.html', {'categories': categories})


def product_list(request, category_id):
    products = client.get_products(category_id)
    return render(request, 'product_list.html', {
        'products': products,
        'category_id': category_id,
        'config_url': Config.URL
    })


def product_detail(request, product_id):
    all_products = client.get_product(product_id)

    if not all_products:
        return HttpResponseNotFound("Товар не найден")

    return render(request, 'product_detail.html', {
        'product': all_products[0],
        'price': all_products[0]['price'],
        'config_url': Config.URL
    })
