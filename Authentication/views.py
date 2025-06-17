from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from Authentication.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from Luabla.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

class ProtectedCardsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cards_list = [
            {'word':'Dog', 'meaning':'Perro', 'example_phrase':'The dog is eating dog food', 'deck_id':'1'},
            {'word':'Car', 'meaning':'Coche', 'example_phrase':'Did you see my car keys? I have to attend to a meeting now', 'deck_id':'2'},
            {'word':'Sugar', 'meaning':'Azucar', 'example_phrase':'Would you like your coffee with sugar?', 'deck_id':'3'},
        ]

        if not cards_list:
            return Response({'error':'Not cards found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message':'Users list is here', 'users':cards_list})


class UsersListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users_list = User.objects.all().values('id', 'username', 'email', 'profile_picture')
        print(users_list)

        if not users_list:
            return Response({'error':'Not users found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'message':'Users list is here', 'users':users_list})

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

        send_mail(
            subject=f"Welcome to Luabla",
            message=f"You´re already on the right way to start learning a new Language, we are really glad that you joined to our community of learners around the world. Keep going, learn, practice and enjoy!. \nIf you have any doubt or question, don´t wait to send us an emal for all your doubts clarification.",
            from_email=EMAIL_HOST_USER, 
            recipient_list=[user.email],
            fail_silently=True, 
        )

        return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)

class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        inputCredential = request.data.get('input')
        password = request.data.get('password')

        try:
            validate_email(inputCredential)
            user = User.objects.filter(email=inputCredential).first()
            username = user.username if user else None
        except ValidationError: 
            username = inputCredential

        user = User.objects.filter(username=username).first()

        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens
        token = TokenObtainPairSerializer.get_token(user)
        access = str(token.access_token)
        refresh = str(token)

        response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        # Set tokens in HTTP-only cookies
        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        return response
    
class SignOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        
        # Clear the HTTP-only JWT cookies
        response.delete_cookie(
            key='access_token' 
        )
        response.delete_cookie(
            key='refresh_token'
        )
        
        return response

class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            user = User.objects.filter(username=user.username).first()
            return Response({
                'username':user.username, 
                'email':user.email, 
                'personal_description':user.personal_description,
                'age':user.age,
                'genre':user.genre,
                'country':user.country,
                'learning_goals':user.learning_goals,
                'profile_picture':user.profile_picture.url,
                'score':user.score,
                'has_picked_language':user.has_picked_language,
                'description':user.description
            }, status=status.HTTP_200_OK)
        except:
            return Response({'error':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)