from django.urls import path
from .views import OrderView

urlpatterns = [
    path('', OrderView.as_view(), name='order-list-create'), 

    path('<int:pk>/', OrderView.as_view(), name='order-detail'), 

    path('<int:pk>/cancel/', OrderView.as_view(), name='order-cancel'), 
]
