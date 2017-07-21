import json

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import (
        ListView,
        View, 
        TemplateView,
        UpdateView,
        CreateView,
        DeleteView,
        DetailView,
        )

from .models import Drink, Ingredient, WebpageURL, Amount
from .forms import PlaylistForm, DrinkBuilderForm
from .utils import youtube_helper
from .tasks import process_youtube_videos

import string

# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {


        }
        return render(request, "cocktail/home.html", context)

    def post(self, request, *args, **kwargs):
        context = {


        }
        return render(request, "cocktail/home.html", context)



class WebpageURLListView(ListView):
    model = WebpageURL
    template_name = 'cocktail/drink_list.html'
    paginate_by = 8
    # cleanup_querysets()

    def get_context_data(self, **kwargs):
        context = super(WebpageURLListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        query = self.request.GET.get("q")
        qs = self.model.objects.all().order_by('-id')
        if query:
            qs = qs.filter(
                    Q(drink__name__icontains=query)

                    )
                   

        return qs


class DrinkCreateView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "form": PlaylistForm
        }
        return render(request, "cocktail/drink_create.html", context)


    def post(self, request, *args, **kwargs):
        form = PlaylistForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data.get("playlist_url")
            process_youtube_videos.delay(link)

        return HttpResponseRedirect(reverse("cocktail:drink"))

class DrinkDeleteView(DeleteView):
    model = Drink
    success_url = reverse_lazy("cocktail:drink")
    template_name = "cocktail/drink_delete.html"

class DrinkDetailView(DetailView):
    queryset = Drink.objects.all()

class IngredientListView(ListView):
    model = Ingredient
    template_name = 'cocktail/ingredient_list.html'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get("q")
        qs = self.model.objects.all().order_by('name')
        if query:
            qs = qs.filter(Q(name__icontains=query))
        return qs

class DrinkBuilderView(View):
    model = Ingredient
    def get(self, request, *args, **kwargs):
        ingredient_list = self.model.objects.all().values_list('name')

        json_dict = json.dumps(list(ingredient_list), cls=DjangoJSONEncoder)

        context = {
            "form": DrinkBuilderForm,
            "test": "A WORD HERE",
            "json_dict": json_dict,

        }
        return render(request, "cocktail/drink_builder.html", context)

    def post(self, request, *args, **kwargs):
        context = {
            "form": DrinkBuilderForm

        }
        return render(request, "cocktail/drink_builder.html", context)

def delete_all_view(request):
    Ingredient.objects.all().delete()
    Drink.objects.all().delete()
    WebpageURL.objects.all().delete()
    AmountIngredient.objects.all().delete()

    return HttpResponseRedirect("/",)

def test(request):
    return render(request, "cocktail/test.html", {})