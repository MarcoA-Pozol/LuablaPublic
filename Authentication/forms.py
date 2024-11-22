from . datasets import COUNTRIES
from django import forms
from . models import User

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=20)
    country = forms.ChoiceField(choices=COUNTRIES)
    profile_picture = forms.ImageField(required=False)
    
    class Meta():
        model = User
        fields = ['username', 'email', 'password', 'country', 'profile_picture']
        
        #Fields like personal description, profile image and age can be setted after profile creation, and score, friends and more will be modified during app using workflow.
    
    """def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if confirm_password != password:
            self.add_error('confirm_password', "Passwords do not match with each other.")
            
        if not password:
            self.add_error('password', "Password was not provided.")
        return cleaned_data"""
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['password'])
        user.email = self.cleaned_data['email']
        user.country = self.cleaned_data['country']
        user.profile_picture = self.cleaned_data['profile_picture']
        
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    