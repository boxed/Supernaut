from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import (
    login,
    logout,
)
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import Template
from django.urls import (
    path,
    include,
)
import debug_toolbar

from iommi import (
    Action,
    Column,
    Form,
    Page,
    Table,
    html,
    Menu,
    MenuItem,
)

from .example_data import setup_example_data
from .models import (
    Album,
    Artist,
    Track,
)

setup_example_data()


# Menu -----------------------------

class SupernautMenu(Menu):
    home = MenuItem(url='/')
    artists = MenuItem()
    albums = MenuItem()
    tracks = MenuItem()

    class Meta:
        attrs__class = {'fixed-top': True}


# Tables ---------------------------

class TrackTable(Table):
    class Meta:
        auto__rows = Track.objects.all().select_related('album__artist')
        columns__name__filter__include = True


class AlbumTable(Table):
    class Meta:
        auto__model = Album
        page_size = 20
        columns__name__cell__url = lambda row, **_: row.get_absolute_url()
        columns__name__filter__include = True
        columns__year__filter__include = True
        columns__year__filter__field__include = False
        columns__artist__filter__include = True
        columns__edit = Column.edit(
            include=lambda request, **_: request.user.is_staff,
        )
        columns__delete = Column.delete(
            include=lambda request, **_: request.user.is_staff,
        )
        actions__create_album = Action(attrs__href='/albums/create/')


class ArtistTable(Table):
    class Meta:
        auto__model = Artist
        columns__name__cell__url = lambda row, **_: row.get_absolute_url()
        columns__name__filter__include = True


# Pages ----------------------------


class IndexPage(Page):
    menu = SupernautMenu()

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

    albums = AlbumTable(
        auto__model=Album,
        tag='div',
        header__template=None,
        cell__tag=None,
        row__template=Template("""
            <div class="card" style="width: 15rem; display: inline-block;" {{ cells.attrs }}>
                <img class="card-img-top" src="/static/album_art/{{ row.artist }}/{{ row.url_name|urlencode }}.jpg">
                <div class="card-body text-center">
                    <h5>{{ cells.name }}</h5>
                    <p class="card-text">
                        {{ cells.artist }}
                    </p>
                </div>
            </div>
        """),
    )


def artist_page(request, artist):
    artist = get_object_or_404(Artist, name=artist)

    class ArtistPage(Page):
        title = html.h1(artist.name)

        albums = AlbumTable(auto__rows=Album.objects.filter(artist=artist))
        tracks = TrackTable(auto__rows=Track.objects.filter(album__artist=artist))

    return ArtistPage()


def album_page(request, artist, album):
    album = get_object_or_404(Album, name=album, artist__name=artist)

    class AlbumPage(Page):
        title = html.h1(album)
        text = html.a(album.artist, attrs__href=album.artist.get_absolute_url())

        tracks = TrackTable(
            auto__rows=Track.objects.filter(album=album),
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
    path('__debug__/', include(debug_toolbar.urls)),

    path('', IndexPage().as_view()),
    path('albums/', AlbumTable(auto__model=Album).as_view()),
    path('albums/create/', Form.create(auto__model=Album).as_view()),
    path('artists/', ArtistTable(auto__model=Artist).as_view()),
    path('tracks/', TrackTable(auto__model=Track).as_view()),

    path('artist/<artist>/', artist_page),
    path('artist/<artist>/<album>/', album_page),
    path('artist/<artist>/<album>/edit/', edit_album),
    path('artist/<artist>/<album>/delete/', delete_album),

    path('log_in/', log_in),
    path('log_out/', log_out),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
