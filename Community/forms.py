from django import forms
from . models import Message

class MessageForm(forms.ModelForm):
    class Meta():
        model = Message
        fields = ['message']
        
    def __init__(self, *args, **kwargs):
        sender = kwargs.pop('sender', None)
        receiver = kwargs.pop('receiver', None)
        super().__init__(*args, **kwargs)
        
    def clean(self):
        """
            Custom data validations
        """
        pass
    
    def save(self, sender, receiver, commit=True):
        message = super().save(commit=False)
        message.sender = sender
        message.receiver = receiver
        message.message = self.cleaned_data['message']
        message.is_read = False
        
        if commit:
            message.save()
        return message