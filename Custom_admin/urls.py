from django.urls import path
from .import views

urlpatterns = [
    path("dashboard/",views.AdminDashboardView.as_view()),
     path("users/",views.AdminUserListView.as_view()),
    path("users/<int:pk>/", views.AdminUserDetailView.as_view()),
    path("users/<int:pk>/status/", views.AdminUserStatusToggleView.as_view()),
     path("orders/", views.AdminOrderListView.as_view()),
    path("orders/<int:pk>/status/",views.AdminOrderStatusUpdateView.as_view()),
    
]

