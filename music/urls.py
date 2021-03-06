from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^play/(?P<song_id>[0-9]+)/$', views.playindex, name='playindex'),
    url(r'^next/$', views.nextindex, name='nextindex'),
    url(r'^prev/$', views.previndex, name='previndex'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    url(r'^create_album/$', views.create_album, name='create_album'),
    url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),
    url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
    url(r'^(?P<album_id>[0-9]+)/play/(?P<song_id>[0-9]+)/$', views.playalbum, name='playAlbum'),
    url(r'^(?P<album_id>[0-9]+)/next/$', views.nextalbum, name='nextAlbum'),
    url(r'^(?P<album_id>[0-9]+)/prev/$', views.prevalbum, name='prevAlbum'),
    url(r'album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name="album_update"),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/play/(?P<song_id>[0-9]+)/$', views.playsongs, name='playsong'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/next/$', views.nextsongs, name='nextsong'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/prev/$', views.prevsongs, name='prevsong'),
    url(r'^updateprofile/$', views.UpdateProfile.as_view(), name='update_profile'),
    url(r'^create_playlist/$',views.create_playlist,name='create_playlist'),
    url(r'^playlists/(?P<filter_by>[a-zA_Z]+)/$', views.playlists, name='playlists'),
    url(r'^playlists/(?P<playlist_id>[0-9]+)/favorite/$', views.favorite_playlist, name='favorite_playlist'),
    url(r'^playlists/(?P<playlist_id>[0-9]+)/delete/$', views.delete_playlist, name='delete_playlist'),
    url(r'^playlists/(?P<playlist_id>[0-9]+)/songs/(?P<filter_by>[a-zA_Z]+)/$', views.playlist_songs,
        name='playlist_songs'),
    url(r'^playlists/(?P<song_id>[0-9]+)/addsong/$', views.add_to_song, name='add_to_playlist'),
    url(r'^playlists/(?P<song_id>[0-9]+)/removesong/$', views.remove_playlist_song, name='remove_song'),
    url(r'^playlists/(?P<playlist_id>[0-9]+)/songs/(?P<filter_by>[a-zA_Z]+)/play/(?P<song_id>[0-9]+)/$',
        views.playplaylist, name='playplaylist'),
    url(r'^playlists/(?P<playlist_id>[0-9]+)/songs/(?P<filter_by>[a-zA_Z]+)/next$',
        views.nextplaylist, name='nextplaylist'),
    url(r'^playlists/(?P<playlist_id>[0-9]+)/songs/(?P<filter_by>[a-zA_Z]+)/prev/$',
        views.prevplaylist, name='prevplaylist'),
    url(r'^playlists/(?P<playlist_id>[0-9]+)/share/$', views.share_playlist, name='share_playlist'),
    url(r'^sharedplaylist/(?P<filter_by>[a-zA_Z]+)/$', views.shared_playlist, name='shared_playlist'),
    url(r'^sharedplaylist/(?P<playlist_id>[0-9]+)/(?P<user_id>[0-9]+)/(?P<filter_by>[a-zA_Z]+)/delete/$',
        views.delete_shared_playlist, name='delete_shared'),
]
