from django.shortcuts import render
from django.urls import path

from .example_data import setup_example_data

setup_example_data()


# Views ----------------------------

def index(request):
    return render(
        request,
        template_name='index.html',
        context=dict(
            content='hello',
            title='Title here!',
        )
    )


# URLs -----------------------------

urlpatterns = [
    path('', index),
]
