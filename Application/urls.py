from django.urls import path
from . import views

urlpatterns = [
    path('setLanguagePicked', views.SetLanguagePicked.as_view(), name='setHasLanguagePicked'),
    path('deck', views.DeckView.as_view(), name='deck'),
    path('chineseDeck', views.ChineseDeckView.as_view(), name='chineseDeck'),
    path('japaneseDeck', views.JapaneseDeckView.as_view(), name='japaneseDeck'),
    path('koreanDeck', views.KoreanDeckView.as_view(), name='koreanDeck'),
]
