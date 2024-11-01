from django.shortcuts import render, HttpResponse, redirect
from Authentication.models import User
from . models import Notifications

def community(request):
    users = User.objects.all().exclude(username=request.user)
    
    context = {"users":users}
    return render(request, "community.html", context)

def chat(request):
    chats = User.objects.all() 
    
    context = {"chats":chats}
    return render(request, "chat.html", context)

def notifications(request):
    user = request.user
    notifications = Notifications.objects.filter(destinatary=user, is_read=False).all()
    
    context = {"notifications":notifications}
    return render(request, "notifications.html", context)

def ACTION_read_notification(request, notification_identifier):
    try:
        notification = Notifications.objects.get(id=notification_identifier)
        
        notification.is_read = True
        notification.save()
        
        return redirect('notifications')
    except Exception as e:
        print(f"Exception {e}")
        return redirect('notifications')