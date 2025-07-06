from django.db import models
from Authentication.models import User
from Decks.models import Deck, ChineseDeck, JapaneseDeck, KoreanDeck

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