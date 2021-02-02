from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkers', views.checkers, name='checkers'),
    # This is for twilio
    path('login', views.login),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='games/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/edit', views.profile_edit, name='profile_edit'),
    path('accounts/profile/view', views.profile_view, name='profile_view'),
    path('people', views.people, name='people'),
    path('add_friends', views.add_friends, name='add_friends'),
    path('change_friends', views.change_friends, name='change_friends'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)