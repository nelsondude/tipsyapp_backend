from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.http import HttpResponse

from .views import (
    HomeView,
    WebpageURLListView,
    DrinkCreateView, 
    IngredientListView, 
    DrinkDeleteView, 
    DrinkDetailView,
    DrinkBuilderView,
    delete_all_view,
    )

app_name="cocktail"

urlpatterns = [
    # url(r'^list/$', DrinkListView.as_view(), name='drink'),
    url(r'^$', HomeView.as_view(), name = 'home'),
    url(r'^list/$', WebpageURLListView.as_view(), name='drink'),
    url(r'^create/$', DrinkCreateView.as_view(), name='create'),
    url(r'^ingredient/$', IngredientListView.as_view(), name='ingredient'),
    url(r'^builder/$', DrinkBuilderView.as_view(), name='builder'),
    url(r'^list/(?P<pk>\d+)/$', DrinkDeleteView.as_view(), name='detail'),
    url(r'^delete/$', delete_all_view, name='delete-all'),

]
