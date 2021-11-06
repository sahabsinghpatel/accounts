from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='singup'),
    path('varify', views.varify, name='varify'),
    path('logout', views.logout_view, name='logout'),
    path('chpass', views.chpass, name='chpass'),
    path('login-with-otp', views.loginWithOTP, name='login-with-otp'),
    path('forgot-password', views.forgot_password, name='forgot-password'),
]
