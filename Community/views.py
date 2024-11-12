from django.shortcuts import render, HttpResponse, redirect
from Authentication.models import User
from . models import Notifications, FriendRequest, Friendship, Message
from django.db.models import Q
from . forms import MessageForm


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
    
    sent_requests = FriendRequest.objects.filter(sender=request.user, accepted=False).all()
    friend_requests = FriendRequest.objects.filter(receiver=request.user, accepted=False).all()

    context = {
        "users": users,
        "friend_request_receivers": friend_request_receivers,
        "friend_request_senders": friend_request_senders,
        "friend_requests": friend_requests,
        "sent_requests": sent_requests
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
        
def ACTION_decline_friend_request(request, friend_request_identifier):
    """
        Decline the received friend request and destroy it. The sender could send another friend requests after this process, but it will be adviced about it was rejected.
    """
    
    if request.method == "POST":
        # Delete friend request instance after rejecting it
        friend_request = FriendRequest.objects.get(id=friend_request_identifier)
        
        # Notificate the sender user about their rejected friend request
        notification = Notifications.objects.create(reason="Friend request rejected", message=f"{friend_request.receiver} has rejected your friend request. This is not your fault, do not worry :)", destinatary=friend_request.sender, is_read=False)
        notification.save()
        
        friend_request.delete()
        
        return redirect('show-friend-requests')
    else:
        return redirect('show-friend-requests')
    
def ACTION_cancel_friend_request(request, friend_request_identifier):
    """
        Cancel a sent friend request. Destroy sent friend request instance.
    """
    
    if request.method == "POST":
        # Get the correct friend request and destroy its instance.
        friend_request = FriendRequest.objects.get(id=friend_request_identifier)
        friend_request.delete()
        return redirect('community')
    else:
        return redirect('community')
    






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

def open_chat(request, chat_identifier):
    """
        Open the chat with one friend, if no any message exists yet, then, the person who open the chat first will sent "Hi" message automatically. Open the chat page and template.
    """
    # Obtain messages for both users
    friend = User.objects.get(id=chat_identifier)
    user = request.user
    user_messages = Message.objects.filter(sender=user, receiver=friend)
    friend_messages = Message.objects.filter(sender=friend, receiver=user)
    
    # Obtain chats
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
        
    
    # Load all messages in conversation in asc order
    messages = Message.objects.filter(Q(sender=user, receiver=friend) | Q(sender=friend, receiver=user)).all().order_by('sent_at')
        
        
    # Send message formulary logic
    if request.method == "POST":
        message_form = MessageForm(request.POST, sender=user, receiver=friend)
        try:
            if message_form.is_valid():
                message = message_form.save(sender=user, receiver=friend, commit=True)
                message.save()
                return redirect('open-chat')
        except Exception as e:
            message_form.add_error('message', f'Error during message sending: {e}')
            print(f'Error during message sending: {e}')
    else:
        message_form = MessageForm(sender=user, receiver=friend)
    
    context = {"user_messages":user_messages, "user":user, "friend_messages":friend_messages, "friend":friend, "chats":chats, "message_form":message_form, "messages":messages}
    
    return render(request, "open_chat.html", context)

def ACTION_send_message(request, user_identifier):
    sender = request.user
    receiver = User.objects.get(id=user_identifier)
    
    if request.method == "POST":
        message_form = MessageForm(request.POST, sender=sender, receiver=receiver)
        try:
            if message_form.is_valid():
                message = message_form.save(sender=sender, receiver=receiver, commit=False)
                message.save()
                return redirect('open-chat')
        except Exception as e:
            message_form.add_error('message', f'Error during message sending: {e}')
            print(f'Error during message sending: {e}')
    else:
        message_form = MessageForm(sender=sender, receiver=receiver)
        
    return render()

# Friends
def ACTION_remove_friend(request, friend_identifier):
    """
        Remove a friend from your friends list and destroy the Friendship object where two users were related to.
    """
    
    if request.method == "POST":
        # Obtain correct friend to be removed.
        friend_to_remove = User.objects.get(id=friend_identifier)
        
        # Obtain the current authenticated user.
        user = request.user
        
        # Obtain Friendship object where two users are related to and delete it.
        try:
            friendship = Friendship.objects.get(Q(user1=friend_to_remove, user2=user) | Q(user1=user, user2=friend_to_remove))
            friendship.delete()
        except Friendship.DoesNotExist:
            print("Friendship does not exist.")
        
        # Obtain FriendRequest object where two users are related to and delete it.
        try:
            friend_request = FriendRequest.objects.get(Q(sender=friend_to_remove, receiver=user) | Q(sender=user, receiver=friend_to_remove))
            friend_request.delete()
        except FriendRequest.DoesNotExist:
            print("Friend request does not exist.")
        
        # Notificate to removed user when he or she is removed for a friendship.
        notification = Notifications.objects.create(reason="Removed for a friendship", message=f"{user} has removed you for your friendship :( But you can search for new ones on the community :)", destinatary=friend_to_remove, is_read=False).save()
        
        return redirect('chat')
    else:
        return redirect('chat')
    






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