from django.db import models
from Authentication.models import User

class Deck(models.Model):
    """
        Deck model structure saved on the DB as 'application.deck' table.
        The current DB is PostgreSQL.
        
        Return:
        -self.title
    """
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    cefr_level = models.CharField(max_length=5, null=True)
    hsk_level = models.CharField(max_length=5, null=True)
    author = models.ForeignKey(User, related_name="deck_author", on_delete=models.CASCADE)
    is_shareable = models.BooleanField(null=False, default=False)
    language = models.CharField(max_length=30, null=False)
    downloads = models.IntegerField(default=0, null=False)
    owners = models.ManyToManyField(User, related_name="deck_owners")
    image = models.ImageField(upload_to="deck_images/", default="deck_images/default_deck_image.jpg", null=False)
    cards_cuantity = models.IntegerField(default=0, null=True)
    
    def __str__(self):
        return self.title


class Card(models.Model):
    """ 
        Deck model structure saved on the DB as 'application.card' table.
        The current DB is PostgreSQL.
        
        Return:
        -self.hanzi
    """
    word = models.CharField(max_length=200, null=True)
    hanzi = models.CharField(max_length=40, null=True)
    pinyin = models.CharField(max_length=120, null=True)
    meaning = models.CharField(max_length=200, null=False)
    example_phrase = models.CharField(max_length=200, null=True)
    author = models.ForeignKey(User, related_name="card_author", on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, related_name="deck", on_delete=models.CASCADE) 
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.hanzi