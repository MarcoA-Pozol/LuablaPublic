from Authentication.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . models import Deck, ChineseDeck, JapaneseDeck, KoreanDeck

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
            author = request.user

            deck = Deck.objects.create(title, description, author, cefr_level, language, is_shareable)
        except Exception as e:
            return Response({'error': f'Error when creating a deck ({e})'}, status=status.HTTP_400_BAD_REQUEST)

        if not deck:
            return Response({'error': 'Deck was not found after creation'}, status=status.HTTP_404_NOT_FOUND)

        deck.save()

        return Response(deck, status=status.HTTP_201_CREATED)
    
class ChineseDeckView(APIView):
    def post(self, request):
        try:
            title = request.data.get('title')
            description = request.data.get('description')
            hsk_level = request.data.get('hskLevel') if request.data.get('hskLevel') else 'HSK1' 
            language = request.data.get('language') if request.data.get('language') else 'ZH'
            is_shareable = request.data.get('isShareable') if request.data.get('isShareable') else False
            author = request.user

            deck = Deck.objects.create(title, description, author, hsk_level, language, is_shareable)
        except Exception as e:
            return Response({'error': f'Error when creating a deck ({e})'}, status=status.HTTP_400_BAD_REQUEST)

        if not deck:
            return Response({'error': 'Deck was not found after creation'}, status=status.HTTP_404_NOT_FOUND)

        deck.save()

        return Response(deck, status=status.HTTP_201_CREATED)

class JapaneseDeckView(APIView):
    def post(self, request):
        try:
            title = request.data.get('title')
            description = request.data.get('description')
            jlpt_level = request.data.get('cefrLevel') if request.data.get('cefrLevel') else 'N5' 
            language = request.data.get('language') if request.data.get('language') else 'JP'
            is_shareable = request.data.get('isShareable') if request.data.get('isShareable') else False
            author = request.user

            deck = Deck.objects.create(title, description, author, jlpt_level, language, is_shareable)
        except Exception as e:
            return Response({'error': f'Error when creating a deck ({e})'}, status=status.HTTP_400_BAD_REQUEST)

        if not deck:
            return Response({'error': 'Deck was not found after creation'}, status=status.HTTP_404_NOT_FOUND)

        deck.save()

        return Response(deck, status=status.HTTP_201_CREATED)
    
class KoreanDeckView(APIView):
    def post(self, request):
        try:
            title = request.data.get('title')
            description = request.data.get('description')
            topik_level = request.data.get('topikLevel') if request.data.get('topikLevel') else 'TOPIK-I-1' 
            language = request.data.get('language') if request.data.get('language') else 'KO'
            is_shareable = request.data.get('isShareable') if request.data.get('isShareable') else False
            author = request.user

            deck = KoreanDeck.objects.create(title, description, author, topik_level, language, is_shareable)
        except Exception as e:
            return Response({'error': f'Error when creating a deck ({e})'}, status=status.HTTP_400_BAD_REQUEST)

        if not deck:
            return Response({'error': 'Deck was not found after creation'}, status=status.HTTP_404_NOT_FOUND)

        deck.save()

        return Response(deck, status=status.HTTP_201_CREATED)