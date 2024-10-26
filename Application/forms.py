from django import forms
from . models import Card, Deck
from . datasets import HSK_LEVELS, CEFR_LEVELS

class CardForm(forms.ModelForm):
    example_phrase = forms.CharField(required=False)
    
    class Meta:
        model = Card
        fields = {'word', 'meaning', 'example_phrase', 'deck'}
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        selected_language = kwargs.pop('language', None)
        super().__init__(*args, **kwargs)
        
        if selected_language == 'Chinese':
            self.fields['hanzi'] = forms.CharField(max_length=255, required=True)
            self.fields['pinyin'] = forms.CharField(max_length=255, required=True)
        
        if user:
            self.fields['deck'].queryset = Deck.objects.filter(author=user)

            
    def save(self, author, commit=True):
        card = super().save(commit=False)
        card.word = self.cleaned_data['word']
        card.meaning = self.cleaned_data['meaning']
        card.example_phrase = self.cleaned_data['example_phrase']
        card.deck = self.cleaned_data['deck'] 
        card.author = author
        
        if commit:
            card.save(author)
        return card
    
class DeckForm(forms.ModelForm):
    cefr_level = forms.ChoiceField(choices=CEFR_LEVELS, required=True)
    image = forms.ImageField(required=False)
    
    class Meta:
        model = Deck
        fields = {'title', 'description', 'cefr_level', 'is_shareable', 'image'}
        
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        selected_language = kwargs.pop('language', None)
        super().__init__(*args, **kwargs)
        
        if selected_language == 'Chinese':
            self.fields['hanzi'] = forms.ChoiceField(choices=HSK_LEVELS, required=True)
        
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = self.author

        if Deck.objects.filter(title=title, author=author).exists():
            raise forms.ValidationError(f'A deck with the title "{title}" by this author "{author}" already exists.')
            print(f'A deck with the title "{title}" by this author "{author}" already exists.')

        return cleaned_data
        
    def save(self, language, commit=True):
        deck = super().save(commit=False)
        deck.title=self.cleaned_data['title']
        deck.description = self.cleaned_data['description']
        deck.cefr_level = self.cleaned_data['cefr_level']
        deck.is_shareable = self.cleaned_data['is_shareable']
        deck.image = self.cleaned_data['image']
        deck.author = self.author
        deck.language = language
        
        if commit:
            deck.save(author=deck.author)
        return deck