from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from .forms import AlbumForm, SongForm, UserForm, PlaylistInfoForm , PlaylistForm
from .models import Album, Song, Playlist, PlaylistInfo
from mutagen.id3 import ID3
import os.path

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

counter = 0
counters = 0


def create_album(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_album.html', context)
            album.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, 'music/create_album.html', context)


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/create_song.html', context)
        audio = ID3(song.audio_file)
        if 'TIT2' in audio:
            song.song_title = audio['TIT2'].text[0]
        else:
            song.song_title = song.audio_file;
        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/create_song.html', context)


def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.filter(user=request.user)
    return render(request, 'music/index.html', {'albums': albums})


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})


def delete_playlist(requset, playlist_id):
    playlist = get_object_or_404(Playlist,pk=playlist_id)
    playlist.delete()
    return render(requset, 'music/playlist.html', {'filter_by': 'all'})


def detail(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        song_list = []
        for s in album.song_set.all():
            song_list.append(s)
        return render(request, 'music/detail.html', {'album': album, 'user': user, 'song_list': song_list})


def playalbum(request, album_id, song_id):
    if not request.user.is_authenticated():
        return render(request,'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album,pk=album_id)
        global counter
        counter = int(song_id);
        song_list = []
        for s in album.song_set.all():
            song_list.append(s)
        song = song_list[counter]
        temp_counter = song.played_counter
        temp_counter += 1
        song.played_counter = temp_counter
        song.save()
        return render(request, 'music/detail.html', {'album': album, 'user': user, 'song_list': song_list, 'curSong': song})


def playsongs(request, filter_by, song_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
            global counters
            counters = int(song_id)
            song = users_songs[counters]
            temp_counter = song.played_counter
            temp_counter += 1
            song.played_counter = temp_counter
            song.save()

        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
            'curSong': song
        })


def nextsongs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
            global counters
            if counters < len(users_songs) - 1:
                counters += 1
                song = users_songs[counters]
            elif counters == len(users_songs) - 1:
                counters += 1
                song = None
            else:
                song = None

        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
            'curSong': song
        })


def nextalbum(request, album_id):
    if not request.user.is_authenticated():
        return render(request,'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album,pk=album_id)
        global counter
        song_list = []
        for s in album.song_set.all():
            song_list.append(s)
        if counter < len(song_list)-1:
            counter += 1
            song = song_list[counter]
        elif counter == len(song_list)-1:
            counter += 1
            song = None
        else:
            song = None
        return render(request, 'music/detail.html', {'album': album, 'user': user, 'song_list': song_list, 'curSong': song})


def prevalbum(request, album_id):
    if not request.user.is_authenticated():
        return render(request,'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album,pk=album_id)
        global counter
        song_list = []
        for s in album.song_set.all():
            song_list.append(s)
        if counter > 0:
            counter -= 1
        elif counter <= 0:
            counter = 0
        song = song_list[counter]
        return render(request, 'music/detail.html', {'album': album, 'user': user, 'song_list': song_list, 'curSong': song})


def prevsongs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
            global counters
            if counters > 0:
                counters -= 1
            elif counters <= 0:
                counters = 0
            song = users_songs[counters]

        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
            'curSong': song
        })


def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    try:
        if playlist.is_favorite:
            playlist.is_favorite = False
        else:
            playlist.is_favorite = True
        playlist.save()
    except (KeyError, Playlist.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'albums': albums,
                'songs': song_results,
            })
        else:
            return render(request, 'music/index.html', {'albums': albums})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)


def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids).order_by('song_title')
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })


def playlists(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            playlist_ids = []
            for playlist in Playlist.objects.filter(user=request.user):
                playlist_ids.append(playlist.pk)
            users_playlist = Playlist.objects.filter(pk__in=playlist_ids).order_by('playlist_name')
            if filter_by == 'favorites':
                users_playlist = users_playlist.filter(is_favorite=True)
        except Playlist.DoesNotExist:
            users_playlist = []
        return render(request, 'music/playlist.html', {
            'playlist_list': users_playlist,
            'filter_by': filter_by,
        })


def playlist_songs(request, filter_by, playlist_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for playlist in Playlist.objects.filter(id=playlist_id):
                for playlistinfo in PlaylistInfo.objects.filter(playlist=playlist):
                    song_ids.append(playlistinfo.song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids).order_by('song_title')
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Playlist.DoesNotExist:
            users_songs = []
        return render(request, 'music/playlist_detail.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
            'playlist_id': playlist_id,
        })


def add_to_song(request, song_id):
    form = PlaylistInfoForm()
    if request.POST:
        playlistinfo = form.save(commit=False)
        playlistinfo.song = get_object_or_404(Song, id=song_id)
        playlistinfo.user = request.user
        playlistinfo.playlist = get_object_or_404(Playlist, id=request.POST['playlist_select'])
        if PlaylistInfo.objects.filter(song = playlistinfo.song).exists() :
            error_message = "Already Added !"
            return render(request, 'music/playlist.html', {'filter_by': 'all', 'error_message': error_message})
        else:
            playlistinfo.save()
        return redirect('music:playlists', 'all')

    playlist_list = Playlist.objects.filter(user=request.user)
    return render(request, 'music/add_to_playlist.html', {'song_id': song_id, 'playlist_list': playlist_list})


class AlbumUpdate(UpdateView):
    form_class = AlbumForm
    model = Album
    template_name = 'music/update_album.html'
    success_url = reverse_lazy('music:index')

    def get_queryset(self):
        return Album.objects.all()


class UpdateProfile(UpdateView):
        form_class = UserForm
        template_name = 'music/update_profile.html'
        success_url = reverse_lazy('music:update_profile')

        def get_object(self, queryset=None):
            return self.request.user


class UpdateSong(UpdateView):
    model = Song
    fields = ['album', 'song_title']
    template_name = 'music/update_song.html'
    success_url = reverse_lazy('music:index')

    def get_queryset(self):
        return Song.objects.all()


def remove_playlist_song(requset, song_id):
    song = get_object_or_404(Song, id=song_id)
    playlistinfo = PlaylistInfo.objects.filter(song=song)
    playlistinfo.delete()
    return redirect('music:playlists', 'all')

