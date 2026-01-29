# products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('categories', views.CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'products/<int:product_id>/reviews/',
        views.ProductReviewView.as_view(),
        name='product-reviews'
    ),
    path(
        'products/<int:product_id>/can-review/',
        views.CanReviewProductView.as_view(),
        name='product-can-review'
    ),
    path(
        'my-reviewable-products/',
        views.UserReviewableView.as_view(),
        name='user-reviewable-products'
    ),
]