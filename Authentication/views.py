from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from Authentication.models import User

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        country = request.data.get('country')
        profile_picture = request.data.get('profile_picture')

        if not profile_picture:
            profile_picture = 'profile_pictures/default_profile_picture.jpg'

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, email=email, password=password, country=country)
        user.save()
        return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)

# from django.shortcuts import render, redirect, HttpResponse
# from . forms import UserRegisterForm, LoginForm
# from django.contrib import auth, messages
# # Email sending 
# from django.core.mail import send_mail
# # Obtain needed variables for emails sending
# from Luabla.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
# print("Luabla email:", EMAIL_HOST_USER)


# def authentication_home(request):
#     return HttpResponse("Welcome to Authentication")

# def register(request):
#     if request.method=="POST":
#         form = UserRegisterForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 #Create new User
#                 user = form.save(commit=False)
#                 user.save()
                
#                 send_mail(
#                     subject=f"Welcome to Luabla",
#                     message=f"You´re already on the right way to start learning a new Language, we are really glad that you joined to our community of learners around the world. Keep going, learn, practice and enjoy!. \nIf you have any doubt or question, don´t wait to send us an emal for all your doubts clarification.",
#                     from_email=EMAIL_HOST_USER, 
#                     recipient_list=[user.email],
#                     fail_silently=True,  # Raise an exception if email sending fails
#                 )

#                 auth.login(request, user)
#                 return redirect('languages-selection')
#             except Exception as e:
#                 form.add_error(None, f"Error during User creation: {e}")
#                 print(f"Error during User creation: {e}")
#     else:
#         form = UserRegisterForm()
#     context = {'form':form}
#     return render(request, "register.html", context)

# def login(request):
#     if request.user.is_authenticated:
#         return redirect('languages-selection')
    
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = auth.authenticate(request, username=username, password=password)
#             if user is not None:
#                 auth.login(request, user)
#                 return redirect('languages-selection')
#             else:
#                 messages.error(request, 'Invalid username or password')
#     else:
#         form = LoginForm()
    
#     context = {'form': form}
#     return render(request, 'login.html', context)

# def logout(request):
#     auth.logout(request)
#     return redirect('welcome')