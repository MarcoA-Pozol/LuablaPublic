from django.shortcuts import render, HttpResponse, redirect
from Authentication.models import User
from . models import Notifications, FriendRequest, Friendship

"""COMMUNITY"""
def community(request):
    remove_this_users = []
    
    friendships = Friendship.objects.filter(user1=request.user) | Friendship.objects.filter(user2=request.user)
    
    for friendship in friendships:
        if friendship.user2 == request.user:
            user = User.objects.get(username=friendship.user1)
            remove_this_users.append(user.id)
        elif friendship.user1 == request.user:
            user = User.objects.get(username=friendship.user2)
            remove_this_users.append(user.id)
        else:
            pass
    remove_this_users.append(request.user.id)
    
    users = User.objects.all().exclude(id__in=remove_this_users)
    

    # Get IDs of users who have received a friend request from the current user
    friend_request_receivers = set(
        FriendRequest.objects.filter(sender=request.user).values_list('receiver_id', flat=True)
    )
    
    # Get IDs of users from who the current user is receiving a friend request
    friend_request_senders = set(
        FriendRequest.objects.filter(receiver=request.user).values_list('sender_id', flat=True)
    )
    
    friend_requests = FriendRequest.objects.filter(receiver=request.user, accepted=False).all()

    context = {
        "users": users,
        "friend_request_receivers": friend_request_receivers,
        "friend_request_senders": friend_request_senders,
        "friend_requests": friend_requests
    }
    return render(request, "community.html", context)

def ACTION_send_friend_request(request, user_identifier):
    """
        Sends a friend request to another user by their ID to identify them.
        Creates a FriendRequest object with 'accepted = False' statement.
        This action does not return nothing, just redirect to a succesful page or reload page if something wrong.
    """
    
    if request.method == "POST":
        sender = request.user 
        receiver = User.objects.get(id=user_identifier)
        accepted = False
        
        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver, accepted=accepted)
        friend_request.save()
        
        return redirect('community')
    else:
        return redirect('community')
    
def show_friend_requests(request):
    """
        Returns all friend request that are sent to you in an html template in a list displaying to be accepted or declined.
    """
    
    user = request.user
    friend_requests = FriendRequest.objects.filter(receiver=user, accepted=False).all()
    
    context = {"friend_requests":friend_requests}
    
    return render(request, "show_friend_requests.html", context)

def ACTION_accept_friend_request(request, friend_request_identifier):
    """
        Creates a relationship when the receiver accept, friendship in this case of one user and another user, the first as the sender of the friend request, and the second user as the receiver.
    """
    
    friend_request = FriendRequest.objects.get(id=friend_request_identifier)
    friend_request.accepted = True
    friend_request.save()
    
    if request.method == "POST":
        friendship = Friendship.objects.create(user1=friend_request.sender, user2=friend_request.receiver) 
        friendship.save()
        
        # Generate a notification to advice to the authenticated user when the receiver of a friend request has accepted it.
        notification = Notifications.objects.create(reason='New friend', message=f"'{friend_request.receiver}' has accepted to be your friend.", destinatary=friend_request.sender, is_read=False)
        notification.save()
        
        return redirect('show-friend-requests')
    else:
        return redirect('show-friend-requests')
        






"""CHAT"""
def chat(request):
    """
        Show users that are friend of the requested user to initialize and chat with them.
        Filter only users that have a Friendship object related to both of them (authenticated user and friend).
    """
    
    friendships = Friendship.objects.all()
    
    chats = []
    for friendship in friendships:
        if friendship.user2 == request.user:
            chat = User.objects.get(username=friendship.user1)
            chats.append(chat)
        elif friendship.user1 == request.user:
            chat = User.objects.get(username=friendship.user2)
            chats.append(chat)
        else:
            pass
    
    context = {"chats":chats}
    return render(request, "chat.html", context)






"""NOTIFICATIONS"""
def show_notifications(request):
    user = request.user
    notifications = Notifications.objects.filter(destinatary=user, is_read=False).all()
    
    context = {"notifications":notifications}
    return render(request, "show_notifications.html", context)

def ACTION_read_notification(request, notification_identifier):
    """
        Set a Notifications object 'is_read' statement to True to hide it from all Notifications dislaying.
    """
    
    try:
        notification = Notifications.objects.get(id=notification_identifier)
        
        notification.is_read = True
        notification.save()
        
        return redirect('show-notifications')
    except Exception as e:
        print(f"Exception {e}")
        return redirect('show-notifications')