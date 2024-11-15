import requests
import json
from django.http import JsonResponse

api_url = "127.0.0.1:8000/luabla_content_api/cards/"

def get_cards(api_url:str):
    response = requests.get(api_url)
    if response.status_code == 200:  # OK: Request has been successful
        dogs = response.json()
        return f"\n[GET] Cards: {dogs}"
    else:
        return f"\n[ERROR] Failed to retrieve cards: {response.status_code}"

print(get_cards(api_url))