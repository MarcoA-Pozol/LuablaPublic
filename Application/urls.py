from django.urls import path
from . import views

urlpatterns = [
    path('/setLanguagePicked', views.SetLanguagePicked.as_view(), name='setHasLanguagePicked'),
    path('/deck', views.DeckView.as_view(), name='deck'),
]
