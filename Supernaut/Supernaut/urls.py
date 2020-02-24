from django.urls import path

from iommi import (
    Table,
)

from .models import Album
from .example_data import setup_example_data

setup_example_data()

# URLs -----------------------------

urlpatterns = [
    path('', Table(auto__model=Album).as_view()),
]
