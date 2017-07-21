
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

# from .views import TweetListView, TweetDetailView, TweetCreateView, TweetUpdateView, TweetDeleteView
from .views import (
    IngredientListAPIView,
    # IngredientUpdateAPIView,
    IngredientDetailAPIView
    )


urlpatterns = [
    url(r'^$', IngredientListAPIView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', IngredientDetailAPIView.as_view(), name='detail'),
]
