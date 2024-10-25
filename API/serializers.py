from Application.models import Deck, Card
from rest_framework import serializers

# Chinese Cards Serializers
class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ['id', 'title', 'description', 'hsk_level', 'author', 'is_shareable', 'image']

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'hanzi', 'pinyin', 'meaning', 'example_phrase', 'author', 'deck']
        
# English Cards Serializers
#.......Implement two serializers for English Cards App (Decks and Cards).......#