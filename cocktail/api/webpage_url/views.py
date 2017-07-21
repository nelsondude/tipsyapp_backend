from rest_framework import generics
from django.db.models import Q
from rest_framework import permissions

from .serializers import WebpageURLModelSerializer
from cocktail.api.pagination import LargeResultsSetPagination, StandardResultsSetPagination
from cocktail.models import Drink, WebpageURL




class WebpageURLListAPIView(generics.ListAPIView):
    serializer_class = WebpageURLModelSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = WebpageURL.objects.all()
        return qs
