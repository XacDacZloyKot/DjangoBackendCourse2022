from django.shortcuts import render

from products.models import Product, ProductCategory


def index(request):
    context = {
        "title": "Store",
    }
    return render(request, "products/index.html", context=context)


def products(request):
    context = {
        "title": "Store - Каталог",
        "products": Product.objects.all(),
        "catigories": ProductCategory.objects.all(),
    }
    return render(request, "products/products.html", context=context)
