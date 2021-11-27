from django.conf import settings
from django.shortcuts import render
from .models import ProductCategory, Product


def index(request):
    products_list = Product.objects.all()[:4]

    context ={
        'title': 'Мой Магазин',
        'products': products_list,
    }

    return render(request, 'mainapp/index.html', context)


def contact(request):
    return render(request, 'mainapp/contact.html')


# links_menu = [
#         {'link_name': 'home', 'name': 'дом'},
#         {'link_name': 'office', 'name': 'офис'},
#         {'link_name': 'modern', 'name': 'модерн'},
#         {'link_name': 'classic', 'name': 'классика'},
#     ]

def products(request, pk=None):
    links_menu = ProductCategory.objects.all()
    context = {
        'links_menu': links_menu,
        'title': 'Товары',
    }
    return render(request, 'mainapp/products.html', context)


# def products_home(request):
#     context = {
#         'links_menu': links_menu,
#         'title': 'Товары'
#     }
#     return render(request, 'mainapp/products.html', context)
#
# def products_office(request):
#     context = {
#         'links_menu': links_menu,
#         'title': 'Товары'
#     }
#     return render(request, 'mainapp/products.html', context)
#
# def products_modern(request):
#     context = {
#         'links_menu': links_menu,
#         'title': 'Товары'
#     }
#     return render(request, 'mainapp/products.html', context)
#
# def products_classic(request):
#     context = {
#         'links_menu': links_menu,
#         'title': 'Товары'
#     }
#     return render(request, 'mainapp/products.html', context)