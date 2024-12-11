from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
# External Models
from Community.models import Notifications
from Authentication.models import User
# Formulary
from . forms import UpdateProfileDataForm
import os
from django.conf import settings

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
            # Get form data
            profile_picture = request.FILES.get('profile_picture')  # Handle file uploads
            learning_goals = request.POST.get('learning_goals', '').strip()
            description = request.POST.get('description', '').strip()

            # Validate and save data 
            if profile_picture:
                # Save the uploaded file
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures/')
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, profile_picture.name)

                with open(file_path, 'wb+') as destination:
                    for chunk in profile_picture.chunks():
                        destination.write(chunk)

                # Update user profile_picture field with the relative path
                user.profile_picture = f"profile_pictures/{profile_picture.name}"

            if learning_goals:
                user.learning_goals = learning_goals
            if description:
                user.description = description
                
            user.save()
        
            # Notificate to authenticated user when their data was changed.
            notification = Notifications.objects.create(reason="Updated data", message=f"Updated profile data.", destinatary=user, is_read=False).save()

            # Return the updated profile image  (This returns the updated files and data to the FrontEnd after it is saved on the DB)
            profile_picture_url = user.profile_picture.url if user.profile_picture else None
            return JsonResponse({
                "message": f"{user} had updated their data.",
                "profile_picture": profile_picture_url,
                "learning_goals": user.learning_goals,
                "description": user.description
            })
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)