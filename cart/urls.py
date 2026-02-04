from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/item/<int:pk>/", views.CartItemDetailView.as_view(), name="cart-item"),
    path("count/",views.CartCountView.as_view(),name="cart-count"),
    path('sample/',views.sampleView.as_view())



    
]