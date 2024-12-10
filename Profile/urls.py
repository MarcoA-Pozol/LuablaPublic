from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_profile, name="user-profile"),
    path('update_profile_data_ajax/', views.update_profile_data_ajax, name="update-profile-data-ajax"),
]
