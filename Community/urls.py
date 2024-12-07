from django.urls import path
from . import views

urlpatterns = [
    # Notifications
    path('show_notifications/', views.show_notifications, name="show-notifications"),
    path('read_notification_ajax/', views.read_notification_ajax, name="read-notification-ajax"),
    path('delete_notification_ajax/', views.delete_notification_ajax, name="delete-notification-ajax")
]
