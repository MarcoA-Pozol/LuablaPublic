from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . models import Deck, ChineseDeck, JapaneseDeck, KoreanDeck
from . serializers import DeckSerializer, ChineseDeckSerializer, JapaneseDeckSerializer, KoreanDeckSerializer


class DeckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        deck_id = request.query_params.get('id')
        language = request.query_params.get('language')
        user = request.user

        if deck_id:
            deck = Deck.objects.filter(id=deck_id).first()
            serialized = DeckSerializer(deck)

            if not deck:
                return Response({'deck':serialized.data}, status=status.HTTP_404_NOT_FOUND)
            return Response({'deck':deck}, status=status.HTTP_200_OK)
        else:
            try:
                serializer = {
                    'ZH': ChineseDeckSerializer,
                    'KO': KoreanDeckSerializer,
                    'JP': JapaneseDeckSerializer
                }.get(language, DeckSerializer)
                deck_model = {
                    'ZH': ChineseDeck,
                    'KO': KoreanDeck,
                    'JP': JapaneseDeck
                }.get(language, Deck)
                decks_list = deck_model.objects.filter(author=user, language=language).all()
                serialized = serializer(decks_list, many=True)

                if len(decks_list) <= 0:
                    return Response({'error':'Decks not found'}, status=status.HTTP_404_NOT_FOUND)
                
                return Response({'decks':serialized.data}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f'Unexpected error ocurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            title = request.data.get('title')
            description = request.data.get('description')
            hsk_level = request.data.get('hskLevel')
            jlpt_level = request.data.get('jlptLevel')
            topik_level = request.data.get('topikLevel')
            cefr_level = request.data.get('cefrLevel')
            language = request.data.get('language') 
            is_shareable = request.data.get('isShareable')
            image = request.FILES.get('image')
            author = request.user
        except Exception as e:
            response = Response({'error': 'Error obtaining request data'}, status=status.HTTP_400_BAD_REQUEST)
            return response

        try:
            if language == 'ZH':
                deck = ChineseDeck.objects.create(title=title, description=description, author=author, is_shareable=True if is_shareable == 'on' else False, image=image, language=language, hsk_level=hsk_level)
            if language == 'JP':
                deck = JapaneseDeck.objects.create(title=title, description=description, author=author, is_shareable=True if is_shareable == 'on' else False, image=image, language=language, jlpt_level=jlpt_level)
            if language == 'KO':
                deck = KoreanDeck.objects.create(title=title, description=description, author=author, is_shareable=True if is_shareable == 'on' else False, image=image, language=language, topik_level=topik_level)
            else:
                deck = Deck.objects.create(title=title, description=description, author=author, is_shareable=True if is_shareable == 'on' else False, image=image, language=language, cefr_level=cefr_level)

            deck.save()
            return Response({'message':'Deck was created'}, status=status.HTTP_201_CREATED)
        except Exception as e: 
            return Response({'error': f'Error during deck creation ({e})'}, status=status.HTTP_400_BAD_REQUEST)

class LibraryDeckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        language = request.query_params.get('language')
        user = request.user

        try:
            serializer = {
                'ZH': ChineseDeckSerializer,
                'KO': KoreanDeckSerializer,
                'JP': JapaneseDeckSerializer
            }.get(language, DeckSerializer)
            deck_model = {
                'ZH': ChineseDeck,
                'KO': KoreanDeck,
                'JP': JapaneseDeck
            }.get(language, Deck)
            decks_list = deck_model.objects.filter(language=language).exclude(author=request.user).exclude(owners=request.user).exclude(cards_quantity=0).all()
            serialized = serializer(decks_list, many=True)

            if len(decks_list) <= 0:
                return Response({'error':'Decks not found'}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({'decks':serialized.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Unexpected error ocurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ChineseDeckView(APIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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