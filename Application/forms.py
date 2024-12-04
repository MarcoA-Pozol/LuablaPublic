from django import forms
from . models import Card, Deck
from . datasets import HSK_LEVELS, CEFR_LEVELS

class CardForm(forms.ModelForm):
    example_phrase = forms.CharField(required=False)
    
    class Meta:
        model = Card
        fields = ['word', 'hanzi', 'pinyin', 'meaning', 'example_phrase', 'deck']
        
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        selected_language = kwargs.pop('language', None)
        super().__init__(*args, **kwargs)
        
        # Add IDs to fields
        self.fields['word'].widget.attrs.update({'id': 'id_word'})
        self.fields['hanzi'].widget.attrs.update({'id': 'id_hanzi'})
        self.fields['pinyin'].widget.attrs.update({'id': 'id_pinyin'})
        self.fields['meaning'].widget.attrs.update({'id': 'id_meaning'})
        self.fields['example_phrase'].widget.attrs.update({'id': 'id_example_phrase'})
        self.fields['deck'].widget.attrs.update({'id': 'id_deck'})
        
        if selected_language == 'Chinese':
            self.fields['hanzi'] = forms.CharField(max_length=255, required=True)
            self.fields['pinyin'] = forms.CharField(max_length=255, required=True)
            self.fields.pop('word', None)
        else:
            self.fields['word'] = forms.CharField(max_length=255, required=True)
            self.fields.pop('hanzi', None)
            self.fields.pop('pinyin', None)
            
        if self.author:
            self.fields['deck'].queryset = Deck.objects.filter(author=self.author, language=selected_language)

            
    def save(self, language, author, commit=True):
        card = super().save(commit=False)
        card.meaning = self.cleaned_data['meaning']
        card.example_phrase = self.cleaned_data['example_phrase']
        card.deck = self.cleaned_data['deck'] 
        card.author = author
        
        if language == "Chinese":
            card.hanzi = self.cleaned_data.get('hanzi')
            card.pinyin = self.cleaned_data.get('pinyin')
        else:
            card.word = self.cleaned_data.get('word')
        
        if commit:
            card.save()
        return card
    
class DeckForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Deck
        fields = ['title', 'description', 'hsk_level', 'cefr_level', 'is_shareable', 'image']

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        selected_language = kwargs.pop('language', None)
        super().__init__(*args, **kwargs)

        if selected_language == 'Chinese':
            self.fields['hsk_level'] = forms.ChoiceField(choices=HSK_LEVELS, required=True)
            self.fields.pop('cefr_level', None)  # Remove cefr_level for Chinese decks
        else:
            self.fields['cefr_level'] = forms.ChoiceField(choices=CEFR_LEVELS, required=True)
            self.fields.pop('hsk_level', None)  # Remove hsk_level for other languages

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = self.author

        if Deck.objects.filter(title=title, author=author).exists():
            raise forms.ValidationError(f'A deck with the title "{title}" by this author "{author}" already exists.')

        return cleaned_data

    def save(self, language, author, commit=True):
        deck = super().save(commit=False)
        deck.title = self.cleaned_data['title']
        deck.description = self.cleaned_data['description']
        deck.is_shareable = self.cleaned_data['is_shareable']
        deck.image = self.cleaned_data['image']
        deck.author = author
        deck.language = language

        if language == "Chinese":
            deck.hsk_level = self.cleaned_data.get('hsk_level')
        else:
            deck.cefr_level = self.cleaned_data.get('cefr_level')

        if commit:
            deck.save()
        return deck