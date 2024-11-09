from django.urls import path
from . import views

urlpatterns = [
    #Community
    path('', views.community, name="community"),
    path('show_friend_requests/', views.show_friend_requests, name="show-friend-requests"),
    path('send_friend_request/<int:user_identifier>/', views.ACTION_send_friend_request, name="action-send-friend-request"),
    path('accept_friend_request/<int:friend_request_identifier>/', views.ACTION_accept_friend_request, name="action-accept-friend-request"),
    path('decline_friend_request/<int:friend_request_identifier>/', views.ACTION_decline_friend_request, name="action-decline-friend-request"),
    path('cancel_friend_request/<int:friend_request_identifier>/', views.ACTION_cancel_friend_request, name="action-cancel-friend-request"),
    #Chat
    path('chat/', views.chat, name="chat"),
    path('open_chat/<int:chat_identifier>/', views.open_chat, name="open-chat"),
    path('action_remove_friend/<int:friend_identifier>/', views.ACTION_remove_friend, name="action-remove-friend"),
    #Notifications
    path('show_notifications/', views.show_notifications, name="show-notifications"),
    path('read_notification/<int:notification_identifier>/', views.ACTION_read_notification, name="action-read-notification")
]
