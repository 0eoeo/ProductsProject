from django.urls import path
from . import views

urlpatterns = [
    path('api/products/', views.get_products, name='get_products'),
    path('api/products/create/', views.create_product, name='create_product'),
    path('', views.product_page, name='product_page'),
]