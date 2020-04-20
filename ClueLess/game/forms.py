
from django import forms
from game.models import Game


class GameForm(forms.ModelForm):
    TYPE_CHOICES = (
        ('Public', 'Public'),
        ('Private', 'Private')
    )

    NUM_PLAYER_CHOICES = (
        ('4', '4'),
        ('5', '5'),
        ('6', '6')
    )

    name = forms.CharField(label="Lobby Name", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    required_players = forms.ChoiceField(label="Numbers of Players to Start the Game",
                            choices=NUM_PLAYER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(label="Lobby Type", choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    private_key = forms.CharField(label="Password", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Game
        fields = ['name', 'type', 'private_key', 'required_players']
