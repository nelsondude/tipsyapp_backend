from django.conf.urls import url

from .views import (
    DrinkListAPIView,
    DrinkDetailAPIView,
    # PossibleDrinksAPIView,
    PlaylistListAPIView,
    UpdateDatabaseAPIView
    )


urlpatterns = [
    url(r'^$', DrinkListAPIView.as_view(), name='list'),
    url(r'^playlists/$', PlaylistListAPIView.as_view(), name='playlists'),
    url(r'^update/$', UpdateDatabaseAPIView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/$', DrinkDetailAPIView.as_view(), name='detail'),
]
