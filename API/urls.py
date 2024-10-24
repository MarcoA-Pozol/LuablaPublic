from django.urls import path
from . import views
#For JWT authentication dependencies
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    #CN_Cards
    path('cn_deck/', views.CnDeck_ListCreate.as_view(), name="CnDeck-ListCreate"),
    path('cn_deck/<int:pk>/', views.CnDeck_RetrieveUpdateDestroy.as_view(), name="CnDeck-RetrieveUpdateDestroy"),
    path('cn_card/', views.CnCard_ListCreate.as_view(), name="CnCard-ListCreate"),
    path('cn_card/<int:pk>/', views.CnCard_RetrieveUpdateDestroy.as_view(), name="CnCard-RetrieveUpdateDestroy"),

    
    #En_Cards
    #....Implement English cards app urls....#
    
    
    # JWT management urls for the Token
    path("token/get/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]


