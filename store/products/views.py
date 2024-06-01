from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from products.models import Product, ProductCategory, Basket


def index(request):
    context = {
        "title": "Store",
    }
    return render(request, "products/index.html", context=context)


def products(request, category_id=None, page_number=1):
    products = (
        Product.objects.filter(category_id=category_id)
        if category_id
        else Product.objects.all()
    )

    per_page = 3
    paginator = Paginator(object_list=products, per_page=per_page)
    products_paginator = paginator.page(page_number)

    context = {
        "title": "Store - Каталог",
        "categories": ProductCategory.objects.all(),
        "products": products_paginator,
    }
    return render(request, "products/products.html", context=context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        baskets.create(product=product, user=request.user, quantity=1)
    else:
        baskets = baskets.first()
        baskets.quantity += 1
        baskets.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
