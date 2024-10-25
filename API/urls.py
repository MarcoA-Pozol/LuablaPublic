from django.urls import path
from . import views
#For JWT authentication dependencies
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    #Cards
    path('deck/', views.Deck_ListCreate.as_view(), name="Deck-ListCreate"),
    path('deck/<int:pk>/', views.Deck_RetrieveUpdateDestroy.as_view(), name="Deck-RetrieveUpdateDestroy"),
    path('card/', views.Card_ListCreate.as_view(), name="Card-ListCreate"),
    path('card/<int:pk>/', views.Card_RetrieveUpdateDestroy.as_view(), name="Card-RetrieveUpdateDestroy"),
    
    # JWT management urls for the Token
    path("token/get/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]


