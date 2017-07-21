from django import forms

class PlaylistForm(forms.Form):
    playlist_url = forms.URLField(label='Youtube Playlist/Channel URL', max_length=1000)

class DrinkBuilderForm(forms.Form):
    drink_search = forms.CharField(max_length=200)