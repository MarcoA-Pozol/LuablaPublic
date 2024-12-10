from django.shortcuts import render, redirect, HttpResponse
from . forms import UserRegisterForm, LoginForm
from django.contrib import auth, messages
# Email sending 
from django.core.mail import send_mail
# Obtain needed variables for emails sending
from Luabla.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
print("Luabla email:", EMAIL_HOST_USER)


def authentication_home(request):
    return HttpResponse("Welcome to Authentication")

def register(request):
    if request.method=="POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                #Create new User
                user = form.save(commit=False)
                user.save()
                
                send_mail(
                    subject=f"Welcome to Luabla {user}!",
                    message=f"You´re already on the right way to start learning a new Language, we are really glad that you joined to our community of learners around the world. Keep going, learn, practice and enjoy!",
                    from_email=EMAIL_HOST_USER,  # Or use DEFAULT_FROM_EMAIL
                    #password=EMAIL_HOST_PASSWORD,
                    recipient_list=[user.email],
                    fail_silently=False,  # Raise an exception if email sending fails
                )

                auth.login(request, user)
                return redirect('languages-selection')
            except Exception as e:
                form.add_error(None, f"Error during User creation: {e}")
                print(f"Error during User creation: {e}")
    else:
        form = UserRegisterForm()
    context = {'form':form}
    return render(request, "register.html", context)

def login(request):
    if request.user.is_authenticated:
        return redirect('languages-selection')
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('languages-selection')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    context = {'form': form}
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('welcome')





"""def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('languages')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    context = {'form': form}
    return render(request, 'login.html', context)
"""