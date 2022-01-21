from ordersapp import views as ordersapp
from django.urls import path

app_name = "ordersapp"

urlpatterns = [
   path('', ordersapp.OrderListView.as_view(), name='list'),
   path('complete/<pk>/', ordersapp.complete, name='complete'),
   path('create/', ordersapp.OrderCreateView.as_view(), name='create'),
   path('read/<pk>/', ordersapp.OrderDetailView.as_view(), name='read'),
   path('update/<pk>/', ordersapp.OrderUpdateView.as_view(), name='update'),
   path('delete/<pk>/', ordersapp.OrderDeleteView.as_view(), name='delete'),
   path('product/<pk>/price/', ordersapp.get_product_price, name='product_price'),

]
