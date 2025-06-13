from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Employees(APIView):
    def get(self, request):
        data = [
            {'id':1, 'name': 'Leonardo Dicrapio'},
            {'id':2, 'name': 'James Cameron'},
            {'id':3, 'name': 'Silvester Stallone'},
        ]
        return Response(data, status=status.HTTP_200_OK)
