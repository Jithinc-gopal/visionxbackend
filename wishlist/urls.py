from django.urls import path
from . import views

urlpatterns = [
   
    path("wishlist/",views.WishlistView.as_view(), name="wishlist"),
    path("count/", views.WishlistCountView.as_view(), name="wishlist-count"),

]   