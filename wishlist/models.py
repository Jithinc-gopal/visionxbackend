from django.db import models
from accounts.models import User
from products.models import Product
 
 
 

# Create your models here.
class WishlistItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="wishlist_items")
    product =models.ForeignKey(Product,on_delete=models.CASCADE,)
    created_at = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ("user","product")
        
    def __str__(self):
        return f"{self.user} - {self.product.title}"    