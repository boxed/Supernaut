from django.shortcuts import get_object_or_404
from django.urls import path
from iommi import (
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
    welcome_text = 'This is a discography of the best acts in music!'

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


# URLs -----------------------------

urlpatterns = [
    path('', IndexPage().as_view()),
    path('albums/', Table(auto__model=Album).as_view()),
    path('artists/', Table(auto__model=Artist).as_view()),
    path('tracks/', Table(auto__model=Track).as_view()),

    path('artist/<artist>/', artist_page),
    path('artist/<artist>/<album>/', album_page),
]
