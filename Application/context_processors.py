def selected_language(request):
    selected_language = request.session.get('selected_language', 'default_language')
    return {'selected_language': selected_language}

def total_notifications(request):
    if request.user.is_authenticated:
        notifications = request.user.notifications.filter(is_read=False)
        total_notifications = len(notifications)
    else:
        total_notifications = 0
        
    return {'total_notifications': total_notifications}

def total_friend_requests(request):
    if request.user.is_authenticated:
        friend_requests = request.user.received_friend_requests.filter(receiver=request.user, accepted=False)
        total_friend_requests = len(friend_requests)
    else:
        total_friend_requests = 0
    
    return {'total_friend_requests': total_friend_requests}