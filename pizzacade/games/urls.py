from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # This is for twilio
    path('login', views.login),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='games/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]