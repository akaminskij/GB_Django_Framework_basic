from django.shortcuts import render, redirect

from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory

from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm

from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class OrderCreateView(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)  # super(OrderItemsCreate, self)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price

            else:
                formset = OrderFormSet()

        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        orderitems = context_data['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)  # super(OrderItemsCreate, self)


class OrderUpdateView(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)  # super(OrderItemsCreate, self)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        orderitems = context_data['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            basket_items = Basket.objects.filter(user=self.request.user)
            basket_items.delete()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)  # super(OrderItemsCreate, self)


class OrderDetailView(DetailView):
    model = Order


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:list')


# @transaction.atomic()
def complete(request, pk):
    order_item = Order.objects.get(pk=pk)
    order_item.status = Order.STSTUS_SENT_TO_PROCEED
    order_item.save()

    # return HttpResponseRedirect(reverse('ordersapp:list'))
    return redirect(OrderDeleteView.as_view())


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_on_save(sender, update_fields, instance, **kwargs):
    # if update_fields is 'quantity' or 'product':
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_on_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
