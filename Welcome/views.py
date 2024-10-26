from django.shortcuts import render, redirect

def welcome(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def languages_selection(request):
    return render(request, 'languages_selection.html')

def ACTION_select_language(request):
    if request.method == 'POST':
        selected_language = request.POST.get('language')
        request.session['selected_language'] = selected_language
        return redirect('application-home') 
    return redirect('application-home')