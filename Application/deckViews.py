from Authentication.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class DeckView(APIView):
    def post(self, request):
        # Complete this logic for Deck creation
        try:
            title = request.data.get('title')
            title = request.data.get('title')
        except Exception as e:
            pass

        if not value:
            pass

        try:
            deck = Deck.object.create(data);
            deck.save()
        except Exception as e:
            pass