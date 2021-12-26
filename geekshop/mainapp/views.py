import random

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product


# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     else:
#         return []


def get_hot_product():
    products_list = Product.objects.all()

    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    same_products_lists = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)

    return same_products_lists[:3]


def index(request):
    products_list = Product.objects.all()[:4]

    context ={
        'title': 'Мой Магазин',
        'products': products_list,
    }

    return render(request, 'mainapp/index.html', context)


def contact(request):
    context = {

    }
    return render(request, 'mainapp/contact.html', context)


def products(request, pk=None, page=1):
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {'name': 'все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        paginator = Paginator(products_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)


        content = {
            'links_menu': links_menu,
            'products': products_paginator,
            'category': category_item,
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()

    context = {
        'links_menu': links_menu,
        'title': 'Товары',
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product),
    }
    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    links_menu = ProductCategory.objects.all()

    context = {
        'links_menu': links_menu,
        'product': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'mainapp/product.html', context)