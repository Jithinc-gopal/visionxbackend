from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10,
                            choices=[('admin','Admin'),('user','User')],
                            default='user'
                            )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=10, 
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Active" )
    
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'


