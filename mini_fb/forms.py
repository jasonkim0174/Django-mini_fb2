from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['firstname', 'lastname', 'city', 'email', 'image_url']


class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']

        