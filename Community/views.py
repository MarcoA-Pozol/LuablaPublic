from django.shortcuts import render, HttpResponse
from Authentication.models import User

def community(request):
    users = User.objects.all().exclude(username=request.user)
    
    context = {"users":users}
    return render(request, "community.html", context)

def chat(request):
    chats = User.objects.all() 
    
    context = {"chats":chats}
    return render(request, "chat.html", context)