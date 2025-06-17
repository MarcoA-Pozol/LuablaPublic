from django.shortcuts import render
from Authentication.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class SetLanguagePicked(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            picked_language = request.data.get('pickedLanguage')

            user = request.user
            user = User.objects.filter(username=user.username, email=user.email).first()

            if not user:
                return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
            response = Response({'message':f'User has picked a language: {picked_language}'}, status=status.HTTP_200_OK)

            user.has_picked_language = True
            user.save()

            return response

        except Exception as e:
            return Response({'error':f'Error when seting hasLanguagePicked: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)