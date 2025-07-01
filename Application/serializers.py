from rest_framework import serializers
from .models import Deck

class DeckSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Deck
        fields = '__all__'