from Application.models import CN_Deck, CN_Card
from rest_framework import serializers

# Chinese Cards Serializers
class CnDeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = CN_Deck
        fields = ['id', 'title', 'description', 'hsk_level', 'author', 'is_shareable', 'image']

class CnCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CN_Card
        fields = ['id', 'hanzi', 'pinyin', 'meaning', 'example_phrase', 'author', 'deck']
        
# English Cards Serializers
#.......Implement two serializers for English Cards App (Decks and Cards).......#