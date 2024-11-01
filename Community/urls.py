from django.urls import path
from . import views

urlpatterns = [
    #Community
    path('', views.community, name="community"),
    path('show_friend_requests/', views.show_friend_requests, name="show-friend-requests"),
    path('send_friend_request/<int:user_identifier>/', views.ACTION_send_friend_request, name="action-send-friend-request"),
    #Chat
    path('chat/', views.chat, name="chat"),
    #Notifications
    path('show_notifications/', views.show_notifications, name="show-notifications"),
    path('read_notification/<int:notification_identifier>/', views.ACTION_read_notification, name="action-read-notification")
]
