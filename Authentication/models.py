from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """All Django builded-in User model fields will be inherited to this model and additionally it will have another custom fields"""
    
    personal_description = models.TextField(null=True, default="I am learning a new language!")
    age = models.IntegerField(null=True, default=0)
    genre = models.CharField(max_length=50, null=True, default="Confident")
    country = models.CharField(max_length=200, null=False)
    learning_goals = models.TextField(null=True, default="Meet new friends and travel around the world!")
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, unique=False, default="profile_pictures/default_profile_picture.jpg")
    score = models.IntegerField(null=False, default=0)
    friends = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='friends_with')
    # App flow fields
    has_picked_language = models.BooleanField(null=True, default=False)
    has_valid_email = models.BooleanField(null=True, default=False)
    description = models.TextField(null=True, default="Hi! I am using Luabla...")


    def __str__(self):
        return self.username

    def add_friend(self, friend_user):
        """Adds a user to the friend list."""
        self.friends.add(friend_user)
    
    def remove_friend(self, friend_user):
        """Removes a user from the friend list."""
        self.friends.remove(friend_user)

    def get_friends(self):
        """Returns the list of friends."""
        return self.friends.all()

    def is_friends_with(self, user):
        """Checks if the user is already friends with another user."""
        return self.friends.filter(id=user.id).exists()
    