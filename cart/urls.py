from django.urls import path
from .views import cart_view
from .views import AddToCartView, RemoveFromCartView

urlpatterns = [
    path('', cart_view, name='cart_view'),
    path('add-to-cart/<str:book_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove/<str:item_id>/', RemoveFromCartView.as_view(), name='delete-from-cart'),
]
