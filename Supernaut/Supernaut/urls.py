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

    artists = Table(auto__model=Artist, page_size=5)
    albums = Table(auto__model=Album, page_size=5)
    tracks = Table(auto__model=Track, page_size=5)


def artist_page(request, artist):
    artist = get_object_or_404(Artist, name=artist)

    class ArtistPage(Page):
        title = html.h1(artist.name)

        albums = Table(auto__rows=Album.objects.filter(artist=artist))
        tracks = Table(auto__rows=Track.objects.filter(album__artist=artist))

    return ArtistPage()


# URLs -----------------------------

urlpatterns = [
    path('', IndexPage().as_view()),
    path('albums/', Table(auto__model=Album).as_view()),
    path('artists/', Table(auto__model=Artist).as_view()),
    path('tracks/', Table(auto__model=Track).as_view()),

    path('artist/<artist>/', artist_page),
]
