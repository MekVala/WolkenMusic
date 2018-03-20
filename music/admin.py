from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Album, Song, Playlist, PlaylistInfo, SharedPlaylist


class MyUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('is_superuser',)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if extra_context is None:

            etc= "select id,song_title,SUM(played_counter) AS sum from music_song " \
                 "where album_id in (select id from music_album where user_id = {0}) " \
                 "group by song_title  having sum >4 LIMIT 10".format(object_id)
            temp = Song.objects.raw(etc)
            songname=[]
            songcount=[]

            for song in temp:
                 songname.append(song.song_title)
                 songcount.append(int(song.sum))

            extra_context = {"songname": songname, "songcount": songcount}
            return super(MyUserAdmin, self).change_view(
                request, object_id=object_id, form_url=form_url, extra_context=extra_context)

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(PlaylistInfo)
admin.site.register(SharedPlaylist)
