from django import forms

class UpdateProfileDataForm(forms.Form):
    profile_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'id': 'id_profile_image',}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your description here...', 'id': 'id_description',}), max_length=500, required=False)
    learning_goals = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Tell and inspire others...', 'id': 'id_description',}), max_length=250, required=False)