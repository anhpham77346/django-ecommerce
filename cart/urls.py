from django.urls import path
from .views import add_to_cart, cart_view

urlpatterns = [
    path('', cart_view, name='cart_view'),
    path('add-to-cart/<str:book_id>/', add_to_cart, name='add_to_cart'),
]
