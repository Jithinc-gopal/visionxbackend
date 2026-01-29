from django.db import models
from accounts.models import User
from products.models import Product

# Create your models here.
class CartItem(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('user','product')
        
    def __str__(self):
        return f"{self.user} - {self.product} ({self.quantity})"
        