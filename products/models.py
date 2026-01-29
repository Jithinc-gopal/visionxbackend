from django.db import models
from accounts.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.URLField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    
    class Meta:
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.title
      
     
      

class Review(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="reviews",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    order_item = models.OneToOneField(  # Change to OneToOne for unique review per order item
        "orders.OrderItem",  # Reference to your order app
        on_delete=models.CASCADE,
        related_name="review",
        null=True,
        blank=True
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Allow multiple reviews from same user on same product, but only through different orders
        constraints = [
            models.UniqueConstraint(
                fields=['order_item'],
                name='unique_review_per_order_item'
            )
        ]
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"Review for {self.product.title} by {self.user.username}"