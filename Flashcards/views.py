from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . models import Flashcard, ChineseFlashcard, JapaneseFlashcard, KoreanFlashcard, RussianFlashcard
from Decks.models import Deck, ChineseDeck, JapaneseDeck, KoreanDeck

class FlashcardView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            language = request.data.get('language')
            word = request.data.get('word')
            hanzi = request.data.get('hanzi')
            pinyin = request.data.get('pinyin')
            kanji = request.data.get('kanji')
            kana = request.data.get('kana')
            romaji = request.data.get('romaji')
            hangul = request.data.get('hangul')
            cyrillic = request.data.get('cyrillic')
            transliteration = request.data.get('transliteration')
            meaning = request.data.get('meaning')
            example_phrase = request.data.get('examplePhrase')
            deck_id = request.data.get('deckId')
            author = request.user
        except Exception as e:
            response = Response({'error': 'Error obtaining request data'}, status=status.HTTP_400_BAD_REQUEST)
            return response
    
        try:
            if language == 'ZH':
                deck = ChineseDeck.objects.get(id=deck_id)
                flashcard = ChineseFlashcard.objects.create(hanzi=hanzi, pinyin=pinyin, meaning=meaning, example_phrase=example_phrase, author=author, deck=deck)
            elif language == 'JP':
                deck = JapaneseDeck.objects.get(id=deck_id)
                flashcard = JapaneseFlashcard.objects.create(kanji=kanji, kana=kana, romaji=romaji, meaning=meaning, example_phrase=example_phrase, author=author, deck=deck)
            elif language == 'KO':
                deck = KoreanDeck.objects.get(id=deck_id)
                flashcard = KoreanFlashcard.objects.create(hangul=hangul, romaji=romaji, meaning=meaning, example_phrase=example_phrase, author=author, deck=deck)
            elif language == 'RU':
                deck = Deck.objects.get(id=deck_id)
                flashcard = RussianFlashcard.objects.create(cyrillic=cyrillic, transliteration=transliteration, meaning=meaning, example_phrase=example_phrase, author=author, deck=deck)
            else:
                deck = Deck.objects.get(id=deck_id)
                flashcard = Flashcard.objects.create(word=word, meaning=meaning, example_phrase=example_phrase, author=author, deck=deck)

            flashcard.save()
            return Response({'message':'Flashcard was created'}, status=status.HTTP_201_CREATED)
        
        except Deck.DoesNotExist:
            return Response({'error': 'Deck not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e: 
            return Response({'error': f'Error during flashcard creation ({e})'}, status=status.HTTP_400_BAD_REQUEST)
