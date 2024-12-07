from django.shortcuts import render, HttpResponse, redirect
from Authentication.models import User
from . models import Notifications, FriendRequest, Friendship, Message
from django.db.models import Q
from . forms import MessageForm
# Load data from a template using AJAX and CSRF token
from django.views.decorators.csrf import csrf_exempt
# JsonResponse for communication with FrontEnd side
from django.http import JsonResponse
import json

"""NOTIFICATIONS"""
def show_notifications(request):
    user = request.user
    notifications = Notifications.objects.filter(destinatary=user, is_read=False).all().order_by("-sent_date")
    read_notifications = Notifications.objects.filter(destinatary=user, is_read=True).all().order_by("-sent_date")
    
    context = {"notifications":notifications, "read_notifications":read_notifications}
    return render(request, "show_notifications.html", context)

def read_notification_ajax(request):
    """
        Save a Notification instance "is_read" statement from False to True.
        This view is called on the FrontEnd side, using AJAX and JQuery to dinamically modify and load the updated content without a page reload.
    """
    
    if request.method == "POST":
        try:
            data = json.loads(request.body) # Parse JSON data from the AJAX request
            notification = Notifications.objects.get(id=data.get('notification_id'))
            
            # Modify the 'is_read' field from the obtained Notifications´s object and save it.
            notification.is_read=True
            notification.save()
            
            return JsonResponse({'message': 'Notification´s "is_read" statement was changed from "False" to "True" successfully!'})
        except Notifications.DoesNotExist:
            return JsonResponse({'error': 'Notification not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def delete_notification_ajax(request):
    """
        Delete a read Notification.
        This delete the notification forever when "delete" button is clicked on FrontEnd side.. 
    """
    
    if request.method == "POST":
        try:
            data = json.loads(request.body) # Parse JSON data from the AJAX request.
            notification = Notifications.objects.get(id=data.get('notification_id')).delete() # Delete the obtained notification
            
            return JsonResponse({'message': 'Notification was deleted successfully!'})
        except Notifications.DoesNotExist:
            return JsonResponse({'error': 'Notification not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method.'}, status=400)