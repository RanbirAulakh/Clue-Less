
from django import forms
from game.models import Game

class GameForm(forms.ModelForm):
    TYPE_CHOICES = (
        ('Public', 'Public'),
        ('Private', 'Private')
    )

    name = forms.CharField(label="Lobby Name", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(label="Lobby Type", choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    # visibility = forms.BooleanField(label="Make it private", widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    # password1 = forms.CharField(label="Password", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Game
        fields = ['name', 'type']