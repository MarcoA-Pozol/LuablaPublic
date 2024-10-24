from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse #This is to set-up a view that works alike an API view to retrieve Cards data in Json format and manage it dinamically with JQuery and AJAX.
import json #Serialize data to a Json String format to manage it on the template and iterate over it or use the data, this will load data before loading page, what is good, but for larger datasets this could not be the most reliable.
from . forms import ChineseCardForm, ChineseDeckForm
from . models import CN_Deck, CN_Card
from Authentication.models import User
from . datasets import HSK_LEVELS
from django.template.loader import render_to_string

@login_required
def chinese_home(request):
    user = request.user 
    context = {'user':user}
    return render(request, 'chinese_home.html', context)





#Studying acquired decks
def chinese_study(request):
    user = request.user
    decks = CN_Deck.objects.filter(owners=user)
    author_decks = CN_Deck.objects.filter(author=user)
    cards = list(CN_Card.objects.values('hanzi', 'pinyin', 'meaning', 'example_phrase'))
    context = {'decks':decks, 'author_decks':author_decks,'cards_json': json.dumps(cards) }
    return render(request, 'chinese_study.html', context)

def ACTION_Study_Deck(request, deck_identifier):
    """Gets the id of the Deck the User wants to study and renders a template with the related Cards."""
    deck = CN_Deck.objects.get(id=deck_identifier)
    deck_cards = CN_Card.objects.filter(deck=deck).values('hanzi', 'pinyin', 'meaning', 'example_phrase')

    context = {
        'deck': deck,
        'deck_cards_json': json.dumps(list(deck_cards)),  # Convert the list of dictionaries to a JSON string
    }
    return render(request, "chinese_study_deck.html", context)









#Discovering and adding new Decks
def chinese_discover(request):
    decks = CN_Deck.objects.all().exclude(author=request.user).exclude(owners=request.user).exclude(cards_cuantity=0)

    titles = CN_Deck.objects.all().values_list('title', flat=True).exclude(cards_cuantity=0).distinct()
    authors = User.objects.exclude(cn_deck_author__cards_cuantity=0).filter(cn_deck_author__isnull=False).distinct().values_list('username', flat=True)
    hsk_levels = HSK_LEVELS
    downloads = ['0', '10', '50', '100', '200', '500', '1000']

    filter_by = request.GET.get('filter_by', 'title')
    selected_option = request.GET.get('option', None)

    # Apply filtering logic
    if filter_by == 'title' and selected_option:
        decks = decks.filter(title=selected_option)
    elif filter_by == 'author' and selected_option:
        decks = decks.filter(author__username=selected_option)
    elif filter_by == 'hsk_level' and selected_option:
        decks = decks.filter(hsk_level=selected_option)
    elif filter_by == 'downloads' and selected_option:
        decks = decks.filter(downloads__gte=int(selected_option))

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
    elif filter_by == 'downloads':
        options = downloads

    context = {
        "decks": decks,
        "options": options,
        "filter_by": filter_by,
        "titles": titles,
        "authors": authors,
        "hsk_levels": hsk_levels,
        "downloads": downloads
    }
    
    return render(request, 'chinese_discover.html', context)

def ACTION_Get_Deck(request, deck_identifier):
    if request.method == "GET":
        user = request.user
        deck = CN_Deck.objects.get(id=deck_identifier)
        deck.owners.add(user)
        deck.downloads = deck.downloads+1
        deck.save()
        return redirect('chinese-discover')
    else:
        return redirect('chinese-discover')
    







#Decks and Cards Creation
def chinese_create(request):
    """Displays two routes to display different formularies, if the user has no any Deck, then it displays the Cards form automatically, if it haves, then displays two buttons to create either of them"""
    return render(request, 'chinese_create.html')

def chinese_create_card(request):
    if request.method == "POST":
        form = ChineseCardForm(request.POST, user=request.user)
        if form.is_valid():
            card = form.save(commit=False, author=request.user)
            deck_identifier = form.cleaned_data['deck']
            card.save()
            
            deck = CN_Deck.objects.get(id=deck_identifier.id)
            deck.cards_cuantity = deck.cards_cuantity+1
            deck.save()
            return redirect('chinese-create-card')
    else:
        form = ChineseCardForm(user=request.user)
        
    context = {'form':form}
    return render(request, 'chinese_create_card.html', context)

def chinese_create_deck(request):
    if request.method == "POST":
        author = request.user
        form = ChineseDeckForm(request.POST, request.FILES, author=author)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.save() 
            return redirect('chinese-create-deck')
    else:
        form = ChineseDeckForm()
    
    context = {'form':form}
    return render(request, 'chinese_create_deck.html', context)