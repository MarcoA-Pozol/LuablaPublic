from django.urls import path, include
# Modules to manage the images routing using static path and files
from django.conf.urls.static import static
from django.conf import settings

base_api_url = 'api/'

urlpatterns = [
    path(f'{base_api_url}/', include('api.urls')),
    path(f'{base_api_url}auth/', include('Authentication.urls')),
    path(f'{base_api_url}app/', include('Application.urls')),
    path(f'{base_api_url}flashcards/', include('Flashcards.urls')),
    path(f'{base_api_url}decks/', include('Decks.urls')),
]

# This is to enable Django to serve media files during development stage.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)