from django.urls import path
from . import views

urlpatterns = [
    path('', views.community, name="community"),
    path('chat/', views.chat, name="chat")
]
