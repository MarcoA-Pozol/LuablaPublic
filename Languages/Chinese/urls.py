from django.urls import path
from . import views

urlpatterns = [
    #Home
    path('', views.chinese_home, name="chinese-home"),
    #Study
    path('study/', views.chinese_study, name="chinese-study"),
    path('study_deck/<int:deck_identifier>/', views.ACTION_Study_Deck, name="cn-action-study-deck"),
    #Discovering
    path('discover/', views.chinese_discover, name="chinese-discover"),
    path('get_deck/<int:deck_identifier>/', views.ACTION_Get_Deck, name="cn-action-get-deck"),
    #Creation
    path('create/', views.chinese_create, name="chinese-create"),
    path('create/deck/', views.chinese_create_deck, name="chinese-create-deck"),
    path('create/card/', views.chinese_create_card, name="chinese-create-card"),
]
