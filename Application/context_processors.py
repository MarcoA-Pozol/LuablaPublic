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