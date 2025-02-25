from django.db import models

class Cart(models.Model):
    customer_id = models.BigIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} - Customer({self.customer_id})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    book_id = models.CharField(max_length=24)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} x Book({self.book_id})"
