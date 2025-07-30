from django.urls import path
from .views import category_list, product_list, load_more_products

urlpatterns = [
    path('', category_list, name='category_list'),
    path('products/<str:category_id>/', product_list, name='product_list'),
    path('load-more/<int:category_id>/<int:page>/', load_more_products, name='load_more_products'),
]
