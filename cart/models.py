from django.db import models


class Cart(models.Model):
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="carts",
    )
    session_key = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return sum(item.get_total_price for item in self.items.all())
    
    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())
    
    def __str__(self):
        return f"Корзина пользователя: {self.user}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    variant = models.ForeignKey("catalog.ProductVariant", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "variant")
    
    @property
    def total_price(self):
        return self.variant.get_price() * self.quantity
    
    def __str__(self):
        return f"Предмет корзины: {self.cart}"

