from django.urls import path
from . import views

urlpatterns = [
    path('', views.authentication_home, name="authentication-home"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout")
]
