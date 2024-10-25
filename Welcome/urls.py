from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name="welcome"),
    path('about/', views.about, name="about"),
    path('languages_selection/',views.languages_selection, name="languages-selection"),
    path('select_language/', views.ACTION_select_language, name="ACTION-select-language"),
]
