from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.application_home, name="application-home"),
    # Study
    path('study/', views.study, name="study"),
    path('study_deck/<int:deck_identifier>/', views.ACTION_Study_Deck, name="action-study-deck"),
    # Discovering
    path('discover/', views.discover, name="discover"),
    path('get_deck_ajax/', views.get_deck_ajax, name="get-deck-ajax"), 
    path('remove_deck_ajax/', views.remove_deck_ajax, name="remove-deck-ajax"),
    # Bank of Cards
    path('bank_of_cards/<int:deck_identifier>/', views.bank_of_cards, name="bank-of-cards"),
    path('get_card_ajax/', views.get_card_ajax, name="get-card-ajax"),
    # Creation
    path('create/', views.create, name="create"),
    path('create/deck/', views.create_deck, name="create-deck"),
    path('create/card/', views.create_card, name="create-card"),
]
