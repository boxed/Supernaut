import json
from pathlib import Path

from django.db import OperationalError

from .models import (
    Album,
    Artist,
    Track,
)


def ensure_objects():
    if not Album.objects.exists():
        with open(Path(__file__).parent.parent / 'scraped_data.json') as f:
            artists = json.loads(f.read())

        for artist_name, albums in artists.items():
            artist, _ = Artist.objects.get_or_create(name=artist_name)
            for album_name, album_data in albums.items():
                album, _ = Album.objects.get_or_create(artist=artist, name=album_name, year=int(album_data['year']))
                for i, (track_name, duration) in enumerate(album_data['tracks']):
                    Track.objects.get_or_create(album=album, index=i+1, name=track_name, duration=duration)


def setup_example_data():
    try:
        ensure_objects()
    except OperationalError:
        # We'll end up here in the management commands before the db is set up
        pass
