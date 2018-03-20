from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Album, Song, Playlist, PlaylistInfo


class MyUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('is_superuser',)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if extra_context is None:
            # Add Here
        return super(MyUserAdmin, self).change_view(
            request, object_id=object_id, form_url=form_url, extra_context=extra_context)

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(PlaylistInfo)
