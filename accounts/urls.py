from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/',views.RegisterView.as_view()),
    path('login/',views.LoginView.as_view()),
    path("profile/",views.ProfileView.as_view()),
    path("forgot-password/", views.ForgotPasswordView.as_view()),
    path("reset-password/<uidb64>/<token>/", views.ResetPasswordView.as_view()),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]  
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
