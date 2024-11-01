from django.urls import path
from . import views

urlpatterns = [
    path('', views.community, name="community"),
    path('chat/', views.chat, name="chat"),
    path('notifications/', views.notifications, name="notifications"),
    path('read_notification/<int:notification_identifier>/', views.ACTION_read_notification, name="action-read-notification")
]
