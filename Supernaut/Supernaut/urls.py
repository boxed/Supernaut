from django.contrib.auth import (
    login,
    logout,
)
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import path
from iommi import (
    Column,
    Form,
    Page,
    Table,
    html,
)

from .example_data import setup_example_data
from .models import (
    Album,
    Artist,
    Track,
)

setup_example_data()


# Pages ----------------------------

class IndexPage(Page):
    title = html.h1('Supernaut')
    welcome_text = html.div('This is a discography of the best acts in music!')

    log_in = html.a(
        'Log in',
        attrs__href='/log_in/',
        include=lambda request, **_: not request.user.is_authenticated,
    )

    log_out = html.a(
        'Log out',
        attrs__href='/log_out/',
        include=lambda request, **_: request.user.is_authenticated,
    )

    artists = Table(
        auto__model=Artist, page_size=5,
        columns__name__cell__url=lambda row, **_: row.get_absolute_url(),
        columns__name__filter__include=True,
    )
    albums = Table(
        auto__model=Album,
        page_size=5,
        columns__name__cell__url=lambda row, **_: row.get_absolute_url(),
        columns__name__filter__include=True,
        columns__year__filter__include=True,
        columns__year__filter__field__include=False,
        columns__artist__filter__include=True,
        columns__edit=Column.edit(
            include=lambda request, **_: request.user.is_staff,
        ),
        columns__delete=Column.delete(
            include=lambda request, **_: request.user.is_staff,
        ),
    )
    tracks = Table(
        auto__model=Track,
        page_size=5,
        columns__name__filter__include=True,
    )


def artist_page(request, artist):
    artist = get_object_or_404(Artist, name=artist)

    class ArtistPage(Page):
        title = html.h1(artist.name)

        albums = Table(
            auto__rows=Album.objects.filter(artist=artist),
            columns__name__cell__url=lambda row, **_: row.get_absolute_url(),
            columns__name__filter__include=True,
            columns__year__filter__include=True,
            columns__year__filter__field__include=False,
            columns__artist__include=False,
        )
        tracks = Table(
            auto__rows=Track.objects.filter(album__artist=artist),
            columns__name__filter__include=True,
        )

    return ArtistPage()


def album_page(request, artist, album):
    album = get_object_or_404(Album, name=album, artist__name=artist)

    class AlbumPage(Page):
        title = html.h1(album)
        text = html.a(album.artist, attrs__href=album.artist.get_absolute_url())

        tracks = Table(
            auto__rows=Track.objects.filter(album=album),
            columns__name__filter__include=True,
            columns__album__include=False,
        )

    return AlbumPage()


def edit_album(request, artist, album):
    album = get_object_or_404(Album, name=album, artist__name=artist)
    return Form.edit(auto__instance=album)


def delete_album(request, artist, album):
    album = get_object_or_404(Album, name=album, artist__name=artist)
    return Form.delete(auto__instance=album)


def log_in(request):
    login(request, User.objects.get())
    return HttpResponseRedirect('/')


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


# URLs -----------------------------

urlpatterns = [
    path('', IndexPage().as_view()),
    path('albums/', Table(auto__model=Album).as_view()),
    path('artists/', Table(auto__model=Artist).as_view()),
    path('tracks/', Table(auto__model=Track).as_view()),

    path('artist/<artist>/', artist_page),
    path('artist/<artist>/<album>/', album_page),
    path('artist/<artist>/<album>/edit/', edit_album),
    path('artist/<artist>/<album>/delete/', delete_album),

    path('log_in/', log_in),
    path('log_out/', log_out),
]
