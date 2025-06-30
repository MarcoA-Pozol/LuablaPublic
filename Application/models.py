from django.db import models
from Authentication.models import User
from . datasets import HSK_LEVELS, CEFR_LEVELS, JLPT_LEVELS, LANGUAGE_CHOICES, TOPIK_LEVELS


# Decks
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

class KoreanDeck(DeckBase): 
    topik_level = models.CharField(max_length=15, null=True, choices=TOPIK_LEVELS, default='TOPIK-I-1') # TOPIK I - 1 - TOPIK II - 6
    language = models.CharField(max_length=2, null=True, default='KO')
    author = models.ForeignKey(User, related_name="korean_deck_author", on_delete=models.CASCADE)
    owners = models.ManyToManyField(User, related_name="korean_deck_owners")



# Flashcards
class FlashcardBase(models.Model):
    meaning = models.CharField(max_length=200, null=False)
    example_phrase = models.CharField(max_length=200, null=True)
    author = models.ForeignKey(User, related_name="flashcard_author", on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, related_name="deck", on_delete=models.CASCADE) 
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    
class Flashcard(FlashcardBase):
    word = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.word

class ChineseFlashcard(FlashcardBase):
    hanzi = models.CharField(max_length=40, null=True)
    pinyin = models.CharField(max_length=120, null=True)
    author = models.ForeignKey(User, related_name="chinese_flashcard_author", on_delete=models.CASCADE)
    deck = models.ForeignKey(ChineseDeck, related_name="chinese_deck", on_delete=models.CASCADE) 

    def __str__(self):
        return self.hanzi
    
class JapaneseFlashcard(FlashcardBase):
    kanji = models.CharField(max_length=50, blank=True, null=True) # Optional (e.g., 食べる)
    kana = models.CharField(max_length=50, null=False) # (e.g., たべる)
    romaji = models.CharField(max_length=100, null=False) # (e.g., "taberu")
    author = models.ForeignKey(User, related_name="japanese_flashcard_author", on_delete=models.CASCADE)
    deck = models.ForeignKey(JapaneseDeck, related_name="japanese_deck", on_delete=models.CASCADE) 
    
    def __str__(self):
        return self.kana
    
class KoreanFlashcard(FlashcardBase):
    hangul = models.CharField(max_length=50, null=False) # (e.g., "먹다")
    romaji = models.CharField(max_length=100, null=False) # (e.g., "meokda")
    author = models.ForeignKey(User, related_name="korean_flashcard_author", on_delete=models.CASCADE)
    deck = models.ForeignKey(KoreanDeck, related_name="korean_deck", on_delete=models.CASCADE) 
    
    def __str__(self):
        return self.hangul
    
class RussianFlashcard(FlashcardBase):
    cyrillic = models.CharField(max_length=50, null=False) # (e.g., "говорить")
    transliteration = models.CharField(max_length=100, null=False)
    author = models.ForeignKey(User, related_name="russian_flashcard_author", on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, related_name="russian_deck", on_delete=models.CASCADE) 

    def __str__(self):
        return self.cyrillic