from Authentication.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . models import Deck

class SetLanguagePicked(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            picked_language = request.data.get('pickedLanguage')

            user = request.user
            user = User.objects.filter(username=user.username, email=user.email).first()

            if not user:
                return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
            response = Response({'message':f'User has picked a language: {picked_language}'}, status=status.HTTP_200_OK)

            user.has_picked_language = True
            user.save()

            return response

        except Exception as e:
            return Response({'error':f'Error when seting hasLanguagePicked: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeckView(APIView):
    def post(self, request):
        try:
            title = request.data.get('title')
            description = request.data.get('description')
            cefr_level = request.data.get('cefrLevel') if request.data.get('cefrLevel') else 'A1' 
            language = request.data.get('language')
            is_shareable = request.data.get('isShareable') if request.data.get('isShareable') else False
        except Exception as e:
            pass

        if not value:
            pass

        try:
            deck = Deck.object.create(data);
            deck.save()
        except Exception as e:
            pass