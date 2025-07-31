from django.urls import path
from .views import category_list, product_list, product_detail

urlpatterns = [
    path('', category_list, name='category_list'),
    path('products/<str:category_id>/', product_list, name='product_list'),
    path('product/<str:product_id>/', product_detail, name='product_detail'),
]
