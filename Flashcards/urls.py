from django.urls import path
from . import views

urlpatterns = [
    path('flashcard', views.FlashcardView.as_view(), name='flashcard'),
]
