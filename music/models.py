from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models


class Album(models.Model):
    GENRE_TYPE =(("Pop", "Pop"), ("Rock", "Rock"), ("Classical", "Classical"), ("Folk", "Folk"), ("Unknown", "Unknown"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100,choices=GENRE_TYPE)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    played_counter = models.IntegerField(default=0)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title


class Playlist(models.Model):
    playlist_name = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.playlist_name


class PlaylistInfo(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    song = models.ForeignKey(Song)
