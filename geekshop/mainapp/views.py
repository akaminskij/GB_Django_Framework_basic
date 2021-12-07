from django.conf import settings
from django.shortcuts import render, get_object_or_404

from mainapp.models import ProductCategory, Product


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

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {'name': 'все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        content = {
            'links_menu': links_menu,
            'products': products_list,
            'category': category_item,
        }
        return render(request, 'mainapp/products_list.html', content)

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