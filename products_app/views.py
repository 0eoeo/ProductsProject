from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from .models import Product
import json


def product_page(request):
    return render(request, 'products.html')


@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')

        # Проверка: название не должно быть пустым
        if not name:
            return JsonResponse({'error': 'Название не может быть пустым'}, status=400)

        # Проверка: цена должна быть положительным числом
        try:
            price = float(price)
            if price <= 0:
                return JsonResponse({'error': 'Цена должна быть больше нуля'}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Некорректная цена'}, status=400)

        # Проверка: продукт с таким названием уже существует
        if Product.objects.filter(name=name).exists():
            return JsonResponse({'error': 'Продукт с таким названием уже существует'}, status=400)

        # Если проверка пройдена, создаем продукт
        product = Product.objects.create(name=name, description=description, price=price)
        return JsonResponse({'message': 'Продукт успешно создан!'}, status=201)

    return JsonResponse({'error': 'Некорректный метод запроса'}, status=405)


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
