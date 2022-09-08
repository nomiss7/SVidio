from django.urls import path
from apps.order import views


urlpatterns = [
    path('', views.cart_list, name='cart_list'),
    path('add/', views.add_to_cart, name='add_to_cart'),
]