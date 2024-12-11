from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
# External Models
from Community.models import Notifications
from Authentication.models import User
# Formulary
from . forms import UpdateProfileDataForm

@login_required
def user_profile(request):
    user = request.user
    form = UpdateProfileDataForm
    context = {"user":user, "form":form}
    return render(request, "user_profile.html", context)

@login_required
def update_profile_data_ajax(request):
    """
        Update user profile data obtaining it from the FrontEnd using AJAX request, and saves it on the DB.
    """

    if request.method == "POST":
        user = request.user
        
        try:
                data = json.loads(request.body) # Parse JSON data from the request(FrontEnd) to be used on this view
                user = User.objects.get(pk=data.get("user_id"))
                
                # Possible data to be updated
                profile_image = data.get("profile_image")
                learning_goals = data.get("learning_goals")
                description = data.get("description")

                # Validate and save data 
                if profile_image != "":
                    user.profile_image = profile_image
                    user.save()
                if learning_goals != "":
                    user.learning_goals = learning_goals
                    user.save()
                if description != "":
                    user.description = description
                    user.save()
            
                # Notificate to authenticated user when their data was changed.
                notification = Notifications.objects.create(reason="Updated data", message=f"Updated profile data.", destinatary=user, is_read=False).save()
                return JsonResponse({"message": f"{user} had updated their data."})
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)