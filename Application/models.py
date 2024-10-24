from django.db import models
from Authentication.models import User

class CN_Deck(models.Model):
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    hsk_level = models.CharField(max_length=5, null=False)
    author = models.ForeignKey(User, related_name="cn_deck_author", on_delete=models.CASCADE)
    is_shareable = models.BooleanField(null=False, default=False)
    language = models.CharField(max_length=30, null=False, default="Chinese")
    downloads = models.IntegerField(default=0, null=False)
    owners = models.ManyToManyField(User, related_name="cn_deck_owners")
    image = models.ImageField(upload_to="deck_images/", default="deck_images/default_deck_image.jpg", null=False)
    cards_cuantity = models.IntegerField(default=0, null=True)
    
    def __str__(self):
        return self.title


class  CN_Card(models.Model):
    hanzi = models.CharField(max_length=40, null=False)
    pinyin = models.CharField(max_length=120, null=False)
    meaning = models.CharField(max_length=200, null=False)
    example_phrase = models.CharField(max_length=200, null=True)
    author = models.ForeignKey(User, related_name="cn_card_author", on_delete=models.CASCADE)
    deck = models.ForeignKey(CN_Deck, related_name="cn_deck", on_delete=models.CASCADE) 
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.hanzi