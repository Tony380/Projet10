from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.LoginFormView.as_view(
        template_name='login.html'), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile')
]

app_name = 'users'
