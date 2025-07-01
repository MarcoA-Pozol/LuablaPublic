from rest_framework import serializers
from .models import Deck, ChineseDeck, JapaneseDeck, KoreanDeck
author = serializers.ReadOnlyField(source='author.username')

class DeckSerializer(serializers.ModelSerializer):
    author = author
    class Meta:
        model = Deck
        fields = '__all__'

class ChineseDeckSerializer(serializers.ModelSerializer):
    author = author
    class Meta:
        model = ChineseDeck
        fields = '__all__'

class JapaneseDeckSerializer(serializers.ModelSerializer):
    author = author
    class Meta:
        model = JapaneseDeck
        fields = '__all__'

class KoreanDeckSerializer(serializers.ModelSerializer):
    author = author
    class Meta:
        model = KoreanDeck
        fields = '__all__'


