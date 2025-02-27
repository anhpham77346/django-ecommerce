from django.urls import path
from .views import cart_view
from .views import AddToCartView

urlpatterns = [
    path('', cart_view, name='cart_view'),
    path('add-to-cart/<str:book_id>/', AddToCartView.as_view(), name='add-to-cart'),
]
