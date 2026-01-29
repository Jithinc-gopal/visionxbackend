from django.db import models
from accounts.models import User
from django.core.validators import RegexValidator


# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )
    
    PAYMENT_CHOICES = (
        ('cash on delivery','Cash on Delivery'),
        ('upi','UPI'),
        ('card','Card')
        
    )
    full_name = models.CharField(max_length=100)
    street_address = models.TextField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=20)
    pincode = models.CharField(max_length=6)
    payment_method = models.CharField(max_length=20,choices=PAYMENT_CHOICES)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    discount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    final_amount = models.DecimalField(max_digits=10,decimal_places=2)
    status =  models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(
    max_length=10,
    validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number')]
)

    
    def __str__(self):
        return f"Order #{self.id} - {self.user}"
    


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    def __str__(self):
        return f"{self.product} x {self.quantity}"
