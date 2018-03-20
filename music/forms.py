from django import forms
from django.contrib.auth.models import User
from .models import Album, Song, PlaylistInfo, Playlist, SharedPlaylist


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['audio_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class PlaylistInfoForm(forms.ModelForm):

    class Meta:
        model = PlaylistInfo
        fields = ['playlist']


class PlaylistForm(forms.ModelForm):

    class Meta:
        model = Playlist
        fields = ['playlist_name']


class SharedPlaylistForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SharedPlaylistForm, self).__init__(*args, **kwargs)
        self.fields['shared'].queryset = self.fields['shared'].queryset.exclude(id=user.id)

    class Meta:
        model = SharedPlaylist
        fields = ['shared']
