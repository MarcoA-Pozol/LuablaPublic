from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def user_profile(request):
    user = request.user
    context = {"user":user}
    return render(request, "user_profile.html", context)