from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse #This is to set-up a view that works alike an API view to retrieve Cards data in Json format and manage it dinamically with JQuery and AJAX.
import json # Serialize data to a Json String format to manage it on the template and iterate over it or use the data, this will load data before loading page, what is good, but for larger datasets this could not be the most reliable.
from . forms import CardForm, DeckForm
from . models import Deck, Card
from Authentication.models import User
# Datasets
from . datasets import HSK_LEVELS, CEFR_LEVELS
from . CardsDatasets.english_cards import ENGLISH_CARDS
from . CardsDatasets.chinese_cards import CHINESE_CARDS
from . CardsDatasets.german_cards import GERMAN_CARDS
from django.template.loader import render_to_string
# Notifications model
from Community.models import Notifications
# Randomize the order of data in a list or JSON
import random
# Connect to API
import requests
# Complex querying
from django.db.models import Q
# Load data from a template using AJAX and CSRF token
from django.views.decorators.csrf import csrf_exempt

@login_required
def application_home(request):
    selected_language = request.session.get('selected_language')
    user = request.user 
    context = {'user':user, 'selected_language':selected_language}
    return render(request, 'application_home.html', context)



# Bank of Cards
@login_required
def bank_of_cards(request, deck_identifier):
    """
        Access to a bank of cards page where the user will be able to select many cards and add them to their decks.
    """
    
    language = request.session.get('selected_language')
    print(f"Selected language from session: {language}")

    if language == "Chinese":
        cards_list = CHINESE_CARDS
    if language == "English":
        cards_list = ENGLISH_CARDS
    if language == "German":
        cards_list = GERMAN_CARDS

    # Author deck
    deck = Deck.objects.get(id=deck_identifier)
    
    # Fetch all cards related to the author deck
    deck_cards = Card.objects.filter(deck=deck)
    
    api_url = "http://localhost:8000/luabla_content_api/cards/" 
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            cards_json = response.json()
        else:
            cards_json = cards_list  # Fallback if API response is not OK
    except:
        cards_json = cards_list  # Fallback if API call fails
        
    # Filter cards to check if they already exists in author deck or not
    filtered_cards = []
    for card in cards_json:
        if language == "Chinese":
            is_duplicate = deck_cards.filter(
                Q(hanzi=card.get("hanzi", "")) & Q(pinyin=card.get("pinyin", ""))
            ).exists()
        else:
            is_duplicate = deck_cards.filter(word=card.get("word", "")).exists()
        
        if not is_duplicate:
            filtered_cards.append(card)
    
    print(cards_list)
    
    cards_json_length = len(filtered_cards)
    random.shuffle(filtered_cards)
    context = {'cards_json': json.dumps(filtered_cards), "language": language, "deck":deck, 'cards_json_length':cards_json_length}
    return render(request, 'bank_of_cards.html', context)

@csrf_exempt
def get_card_ajax(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data from the request
            deck = Deck.objects.get(id=data.get("deck_id"))

            # Create and save the card
            card = Card.objects.create(
                word=data.get("word", ""),
                hanzi=data.get("hanzi", ""),
                pinyin=data.get("pinyin", ""),
                meaning=data.get("meaning", ""),
                example_phrase=data.get("example_phrase", ""),
                author=request.user,
                deck=deck,
            )
            # Update number of cards in the deck.
            deck.cards_cuantity = deck.cards_cuantity+1
            deck.save()
            return JsonResponse({"message": "Card saved successfully!"})
        except Deck.DoesNotExist:
            return JsonResponse({"error": "Deck not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)

#Studying acquired decks
@login_required
def study(request):
    user = request.user
    language = request.session.get('selected_language')
    decks = Deck.objects.filter(owners=user, language=language)
    author_decks = Deck.objects.filter(author=user, language=language)
    cards = list(Card.objects.values('hanzi', 'pinyin', 'meaning', 'example_phrase'))
    context = {'decks':decks, 'author_decks':author_decks,'cards_json': json.dumps(cards) }
    return render(request, 'study.html', context)

@login_required
def ACTION_Study_Deck(request, deck_identifier):
    """Gets the id of the Deck the User wants to study and renders a template with the related Cards."""
    deck = Deck.objects.get(id=deck_identifier)
    language = request.session.get("selected_language")
    if language == "Chinese":
        deck_cards = Card.objects.filter(deck=deck).values('hanzi', 'pinyin', 'meaning', 'example_phrase')
    else:
        deck_cards = Card.objects.filter(deck=deck).values('word', 'meaning', 'example_phrase')
    
    # Serialize obtained list of cards as a JSON
    deck_cards_list = list(deck_cards)
    random.shuffle(deck_cards_list)
    deck_cards_json = json.dumps(deck_cards_list)
    
    print("Final JSON: ", deck_cards_json)
    
    context = {
        'deck': deck,
        'language': language,
        'deck_cards_json': deck_cards_json  
    }
    return render(request, "study_deck.html", context)





#Discovering and adding new Decks
@login_required
def discover(request):
    """
        Load deck options on the Library to be acquired by the requested user.
        It filters the decks by the selected language, excluding those that have the current user as an author and those that does not have a single card yet. This uses a filtering bar to filter by title, author and hsk/cefr levels.
        
        Parametters:
            -Nothing
            
        Return:
            -Renderize 'discover' page.
    """
    language = request.session.get('selected_language')
    decks = Deck.objects.filter(language=language).exclude(author=request.user).exclude(owners=request.user).exclude(cards_cuantity=0)

    titles = Deck.objects.filter(language=language).values_list('title', flat=True).exclude(cards_cuantity=0).exclude( author=request.user).exclude(owners=request.user).distinct()
    authors = User.objects.filter(deck_author__language=language).exclude(deck_author__cards_cuantity=0).exclude(username=request.user).filter(deck_author__isnull=False).distinct().values_list('username', flat=True).filter(deck_author__in=decks)
    hsk_levels = HSK_LEVELS
    cefr_levels = CEFR_LEVELS

    filter_by = request.GET.get('filter_by', 'title')
    selected_option = request.GET.get('option', None)

    # Apply filtering logic
    if filter_by == 'title' and selected_option:
        decks = decks.filter(title=selected_option)
    elif filter_by == 'author' and selected_option:
        decks = decks.filter(author__username=selected_option)
    elif filter_by == 'hsk_level' and selected_option:
        decks = decks.filter(hsk_level=selected_option)
    elif filter_by == 'cefr_level' and selected_option:
        decks = decks.filter(cefr_level=selected_option)

    # Check if it's an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/_deck_list.html', {'decks': decks})
        return JsonResponse({'html': html})

    # Normal request
    options = []
    if filter_by == 'title':
        options = list(titles)
    elif filter_by == 'author':
        options = list(authors)
    elif filter_by == 'hsk_level':
        options = [level[1] for level in HSK_LEVELS]
    elif filter_by == 'cefr_level':
        options = [level[1] for level in CEFR_LEVELS]

    context = {
        "language": language,
        "decks": decks,
        "options": options,
        "filter_by": filter_by,
        "titles": titles,
        "authors": authors,
        "hsk_levels": hsk_levels,
        "cefr_levels": cefr_levels,
    }
    
    return render(request, 'discover.html', context)

@login_required
def ACTION_Get_Deck(request, deck_identifier):
    if request.method == "GET":
        language = request.session.get('selected_language')
        user = request.user
        deck = Deck.objects.get(id=deck_identifier)
        deck.owners.add(user)
        deck.downloads = deck.downloads+1
        deck.save()
        
        obtained_deck_notification = Notifications.objects.create(reason='Obtained deck', message=f"'{deck}' deck from {language} language has been obtained and is now available to be studied.", destinatary=user, is_read=False)
        obtained_deck_notification.save()
        return redirect('study')
    else:
        return redirect('study')
    







#Decks and Cards Creation
@login_required
def create(request):
    """Displays two routes to display different formularies, if the user has no any Deck, then it displays the Cards form automatically, if it haves, then displays two buttons to create either of them"""
    return render(request, 'create.html')

@login_required
def create_card(request):
    author = request.user
    language = request.session.get('selected_language')
    
    if request.method == "POST":
        form = CardForm(request.POST, author=author, language=language)
        if form.is_valid():
            card = form.save(commit=True, language=language, author=author)
            deck_identifier = form.cleaned_data['deck']
            card.save()
            
            deck = Deck.objects.get(id=deck_identifier.id)
            deck.cards_cuantity = deck.cards_cuantity+1
            deck.save()
            return redirect('create-card')
    else:
        form = CardForm(author=author, language=language)
        
    context = {'form':form}
    return render(request, 'create_card.html', context)

@login_required
def create_deck(request):
    author = request.user
    language = request.session.get('selected_language')

    if request.method == "POST":
        form = DeckForm(request.POST, request.FILES, author=author, language=language)
        if form.is_valid():
            deck = form.save(commit=True, language=language, author=author)
            return redirect('create-deck')
    else:
        form = DeckForm(author=author, language=language)
    
    context = {'form': form}
    return render(request, 'create_deck.html', context)