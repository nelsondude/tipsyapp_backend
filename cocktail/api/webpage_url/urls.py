
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

# from .views import TweetListView, TweetDetailView, TweetCreateView, TweetUpdateView, TweetDeleteView
from .views import (
    WebpageURLListAPIView,
    )

app_name='cocktail'

urlpatterns = [
    url(r'^$', WebpageURLListAPIView.as_view(), name='list'),
]
