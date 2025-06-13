# from django.shortcuts import render
# # Packages for customized APIs
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAdminUser, IsAuthenticated
# from rest_framework.views import APIView
# from django.db import transaction
# from django.db.models import F
# # Generic API views
# from rest_framework import generics
# # Serializers
# from . serializers import CardSerializer, DeckSerializer
# # User model
# from Authentication.models import User
# # Languages models
# from Application.models import Deck, Card

# # API Views    
# class Deck_ListCreate(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated, IsAdminUser]
#     serializer_class = DeckSerializer
#     queryset = Deck.objects.all()
    
# class Deck_RetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated, IsAdminUser]
#     serializer_class = DeckSerializer
#     queryset = Deck.objects.all()

# class Card_ListCreate(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated, IsAdminUser]
#     serializer_class = CardSerializer
#     queryset = Card.objects.all()

#     def create(self, request, *args, **kwargs):
#         data = request.data

#         # Using atomic transaction to ensure all-or-nothing behavior
#         with transaction.atomic():
#             # Check if the data is a list
#             if isinstance(data, list):
#                 errors = []
#                 created_cards = []
#                 deck_id = None

#                 # Loop through each item in the list
#                 for item in data:
#                     serializer = self.get_serializer(data=item)
#                     if serializer.is_valid():
#                         created_card = serializer.save()
#                         created_cards.append(created_card)

#                         # Increase the number of cards in the related deck
#                         deck_id = item['deck']
#                         Deck.objects.filter(id=deck_id).update(cards_cuantity=F('cards_cuantity') + 1)
#                     else:
#                         errors.append(serializer.errors)

#                 if errors:
#                     # If there are any errors, rollback the transaction and return errors
#                     transaction.set_rollback(True)
#                     return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

#                 # Return the created cards
#                 return Response(self.get_serializer(created_cards, many=True).data, status=status.HTTP_201_CREATED)

#             # Fallback to single card creation (when data is not a list)
#             return super().create(request, *args, **kwargs)

    
# class Card_RetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated, IsAdminUser]
#     serializer_class = CardSerializer
#     queryset = Card.objects.all()