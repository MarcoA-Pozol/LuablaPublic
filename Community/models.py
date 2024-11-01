from django.db import models
from Authentication.models import User
        
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('sender', 'receiver')  # Prevent duplicate requests

    def accept(self):
        """Accept the friend request and add both users to each other's friend list."""
        self.receiver.friends.add(self.sender)
        self.sender.friends.add(self.receiver)
        self.accepted = True
        self.save()
        
    def decline(self):
        """Decline the friend request."""
        self.delete() 
        
    def __str__(self):
        return f"{self.sender} sent a friend request to {self.receiver}"
    

class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend1_set')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend2_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')  # Prevent duplicate friendships

    def __str__(self):
        return f"{self.user1} is friends with {self.user2}"
    
    
    
# Notifications model
class Notifications(models.Model):
    reason = models.CharField(max_length=200, unique=False, null=True)
    message = models.TextField()
    destinatary = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    sent_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.message
    
    