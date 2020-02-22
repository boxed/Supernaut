from django.shortcuts import render
from django.urls import path

from iommi import (
    Table,
    Column,
)

from .models import Album
from .example_data import setup_example_data

setup_example_data()


# Tables ---------------------------

class AlbumsTable(Table):
    name = Column()
    artist = Column()
    year = Column()


# Views ----------------------------

def index(request):
    return render(
        request,
        template_name='index.html',
        context=dict(
            content=AlbumsTable(
                rows=Album.objects.all(),
            ).bind(request=request),
            title='Title here!',
        )
    )


# URLs -----------------------------

urlpatterns = [
    path('', index),
]
