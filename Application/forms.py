from django import forms
from . models import Card, Deck
from . datasets import HSK_LEVELS

class CardForm(forms.ModelForm):
    example_phrase = forms.CharField(required=False)
    
    class Meta:
        model = Card
        fields = {'hanzi', 'pinyin', 'meaning', 'example_phrase', 'deck'}
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['deck'].queryset = Deck.objects.filter(author=user)

            
    def save(self, author, commit=True):
        card = super().save(commit=False)
        card.hanzi = self.cleaned_data['hanzi']   
        card.pinyin = self.cleaned_data['pinyin']
        card.meaning = self.cleaned_data['meaning']
        card.example_phrase = self.cleaned_data['example_phrase']
        card.deck = self.cleaned_data['deck'] 
        card.author = author
        
        if commit:
            card.save(author)
        return card
    
class DeckForm(forms.ModelForm):
    hsk_level = forms.ChoiceField(choices=HSK_LEVELS, required=False)
    image = forms.ImageField(required=False)
    
    class Meta:
        model = Deck
        fields = {'title', 'description', 'hsk_level', 'is_shareable', 'image'}
        
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super().__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = self.author

        if Deck.objects.filter(title=title, author=author).exists():
            raise forms.ValidationError(f'A deck with the title "{title}" by this author "{author}" already exists.')
            print(f'A deck with the title "{title}" by this author "{author}" already exists.')

        return cleaned_data
        
    def save(self, commit=True):
        deck = super().save(commit=False)
        deck.title=self.cleaned_data['title']
        deck.description = self.cleaned_data['description']
        deck.hsk_level = self.cleaned_data['hsk_level']
        deck.is_shareable = self.cleaned_data['is_shareable']
        deck.image = self.cleaned_data['image']
        deck.author = self.author
        
        if commit:
            deck.save(author=deck.author)
        return deck