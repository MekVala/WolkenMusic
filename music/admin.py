from django.contrib import admin
from .models import Album, Song, Playlist, PlaylistInfo

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(PlaylistInfo)



