"""Description: Contains the MatchForm class, a Django ModelForm for creating or editing Match instances.
             Automatically generates form fields based on the Match model and includes a custom time 
             field with a specific widget for user input."""


from django import forms
from .models import Match

class MatchForm(forms.ModelForm):
    """
    A form for creating or editing Match instances. It uses the Django ModelForm
    to automatically generate form fields based on the Match model.
    """
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=False  
    )

    class Meta:
        """
        Meta options for the MatchForm class. Specifies the model to use for the form
        and the fields to include in the form.
        """
        model = Match
        fields = ['home_team', 'away_team', 'date', 'time', 'home_score', 'away_score', 'status']
