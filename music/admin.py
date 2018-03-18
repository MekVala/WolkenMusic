from django.contrib import admin
from .models import Album, Song, Playlist, PlaylistInfo, PlayedSummery

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(PlaylistInfo)


@admin.register(PlayedSummery)
class PlayedSummerAdmin(admin.ModelAdmin):
    change_list_template = 'admin/playedsong_summery.html'



