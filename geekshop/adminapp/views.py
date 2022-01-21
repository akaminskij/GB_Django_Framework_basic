from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users_list.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'form': user_form
    }

    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    # ShopUserAdminEditForm
    title = 'пользователи/изменение'
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserAdminEditForm(instance=current_user)

    context = {
        'title': title,
        'form': user_form
    }

    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'

    current_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        current_user.is_active = False
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))

    context = {
        'title': title,
        'object': current_user,
    }

    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    # categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects_list': ProductCategory.objects.all()
    }

    return render(request, 'adminapp/categories_list.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'Категории/создание'
#
#     if request.method == 'POST':
#         form = ProductCategoryEditForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         form = ProductCategoryEditForm()
#
#     context = {
#         'title': title,
#         'form': form
#     }
#
#     return render(request, 'adminapp/category_form.html', context)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    success_url = reverse_lazy('adminapp:categories')
    # fields = '__all__'
    form_class = ProductCategoryEditForm


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'Категории/редактирование'
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         form = ProductCategoryEditForm(request.POST, instance=category_item)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         form = ProductCategoryEditForm(instance=category_item)
#
#     context = {
#         'title': title,
#         'form': form
#     }
#
#     return render(request, 'adminapp/category_form.html', context)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    success_url = reverse_lazy('adminapp:categories')
    # fields = '__all__'
    form_class = ProductCategoryEditForm


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'Категории/удаление'
#     current_category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         # user.delete()
#         # вместо удаления лучше сделаем неактивным
#         current_category.is_active = False
#         current_category.save()
#         return HttpResponseRedirect(reverse('adminapp:categories'))
#
#     context = {
#         'title': title,
#         'object': current_category,
#     }
#
#     return render(request, 'adminapp/category_delete.html', context)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')

    # def delete(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     self.object.is_active = False
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'
    category_item = get_object_or_404(ProductCategory, pk=pk)

    context = {
        'title': title,
        'category': category_item,
        'object_list': Product.objects.filter(category__pk=pk)
    }

    return render(request, 'adminapp/products_list.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     title = 'Продукты/добавление'
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES )
#         if product_form.is_valid():
#             product_item = product_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[product_item.category.pk]))
#     else:
#         product_form = ProductEditForm()
#
#     context = {
#         'title': title,
#         'form': product_form,
#         'category': category_item,
#     }
#
#     return render(request, 'adminapp/product_form.html', context)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('adminapp:categories')

    def _get_category(self):
        category_id = self.kwargs.get('pk')
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        return category_item

    def get_success_url(self):
        return reverse('adminapp:products', args=[self._get_category().pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context_data['category'] = self._get_category()
        return context_data


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'Продукты/просмотр'
#     product_item = get_object_or_404(Product, pk=pk)
#
#     context = {
#         'title': title,
#         'object': product_item,
#     }
#
#     return render(request, 'adminapp/product_read.html', context)


class  ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'Продукты/редактирование'
    product_item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES, instance=product_item)
        if product_form.is_valid():
            product_item = product_form.save()
            return HttpResponseRedirect(reverse('adminapp:products', args=[product_item.category.pk]))
    else:
        product_form = ProductEditForm(instance=product_item)

    context = {
        'title': title,
        'form': product_form,
        'category': product_item.category,
    }

    return render(request, 'adminapp/product_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'Продукт/удаление'
    product_item = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        product_item.is_active = False
        product_item.save()
        return HttpResponseRedirect(reverse('adminapp:products', args=[product_item.category.pk]))

    context = {
        'title': title,
        'object': product_item,
    }

    return render(request, 'adminapp/product_delete.html', context)
