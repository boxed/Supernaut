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


# URLs -----------------------------

urlpatterns = [
    path('', IndexPage().as_view()),
    path('albums/', Table(auto__model=Album).as_view()),
    path('artists/', Table(auto__model=Artist).as_view()),
    path('tracks/', Table(auto__model=Track).as_view()),
]
