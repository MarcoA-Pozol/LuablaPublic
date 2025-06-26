from django.db import models
from Authentication.models import User
from . datasets import HSK_LEVELS, CEFR_LEVELS, JLPT_LEVELS, LANGUAGE_CHOICES

class DeckBase(models.Model):
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    author = models.ForeignKey(User, related_name="deck_author", on_delete=models.CASCADE)
    is_shareable = models.BooleanField(null=True, default=False)
    image = models.ImageField(upload_to="deck_images/", default='deck_images/default_deck_image.jpg', null=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null=True, default='EN')
    owners = models.ManyToManyField(User, related_name="deck_owners")
    downloads = models.IntegerField(default=0, null=True)
    cards_quantity = models.IntegerField(default=0, null=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Deck(DeckBase):
    cefr_level = models.CharField(max_length=5, null=True, choices=CEFR_LEVELS, default='A1') # A1 - C2
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null=True, default='EN')

class ChineseDeck(DeckBase):
    hsk_level = models.CharField(max_length=5, null=True, choices=HSK_LEVELS, default='HSK1') # HSK1 - HSK6
    language = models.CharField(max_length=2, null=True, default='ZH')
    author = models.ForeignKey(User, related_name="chinese_deck_author", on_delete=models.CASCADE)
    owners = models.ManyToManyField(User, related_name="chinese_deck_owners")


class JapaneseDeck(DeckBase): 
    jlpt_level = models.CharField(max_length=5, null=True, choices=JLPT_LEVELS, default='N5') # N5 - N1
    language = models.CharField(max_length=2, null=True, default='JP')
    author = models.ForeignKey(User, related_name="japanese_deck_author", on_delete=models.CASCADE)
    owners = models.ManyToManyField(User, related_name="japanese_deck_owners")