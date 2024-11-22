from django.shortcuts import render, redirect
from Authentication.models import User

def welcome(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def languages_selection(request):
    # Auth user
    user = User.objects.get(username=request.user)
    if user.language_picked == False:
        return render(request, 'languages_selection.html')
    else:
        return redirect('study')

def ACTION_select_language(request):
    # Auth user
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        selected_language = request.POST.get('language')
        request.session['selected_language'] = selected_language
        user.language_picked = True
        user.save()
        return redirect('study') 
    return redirect('study')