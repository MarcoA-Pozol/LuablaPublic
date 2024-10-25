from django.urls import path
from . import views

urlpatterns = [
    #Home
    path('', views.application_home, name="application-home"),
    #Study
    path('study/', views.study, name="study"),
    path('study_deck/<int:deck_identifier>/', views.ACTION_Study_Deck, name="action-study-deck"),
    #Discovering
    path('discover/', views.discover, name="discover"),
    path('get_deck/<int:deck_identifier>/', views.ACTION_Get_Deck, name="action-get-deck"),
    #Creation
    path('create/', views.create, name="create"),
    path('create/deck/', views.create_deck, name="create-deck"),
    path('create/card/', views.create_card, name="create-card"),
]
