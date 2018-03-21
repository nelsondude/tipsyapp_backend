from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model
from django.core import serializers
from rest_framework.response import Response
import json
from .utils import getDrinks, getCountedDrinks

from django.db.models import Count, Q




from cocktail.api.pagination import (
    LargeResultsSetPagination,
    StandardResultsSetPagination
)
from cocktail.models import Drink, Playlist, Ingredient
from .serializers import (
    DrinkListModelSerializer,
    DrinkDetailModelSerializer,
    PlaylistModelSerializer,
)

from cocktail.tasks import process_youtube_videos

User = get_user_model()

class UpdateDatabaseAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self, request, *args, **kwargs):
        process_youtube_videos.delay()
        return Response({'updating': True}, status=200)


class PlaylistListAPIView(ListAPIView):
    serializer_class = PlaylistModelSerializer
    permission_classes = [AllowAny]
    queryset = Playlist.objects.all().order_by('name').filter(visible=True)
    pagination_class = LargeResultsSetPagination


class DrinkDetailAPIView(UpdateModelMixin, RetrieveAPIView):
    queryset = Drink.objects.all()
    serializer_class = DrinkDetailModelSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def get_object(self):
        obj = super(DrinkDetailAPIView, self).get_object()
        changeUser = self.request.GET.get('changeUser')
        user = self.request.user
        print(changeUser, user)
        if user.is_authenticated:
            qs = User.objects.filter(username=user.username)
            if qs.exists() and qs.count() == 1 and changeUser:
                user_obj = qs.first()
                if obj.user.all().filter(username=user_obj.username).exists():
                    obj.user.remove(user_obj)
                else:
                    obj.user.add(user_obj)
                obj.save()
        return obj

class DrinkListAPIView(ListAPIView):

    serializer_class = DrinkListModelSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        userQuery = self.request.GET.get('user')
        query = self.request.GET.get("q")
        filters = self.request.GET.getlist('filter')
        order = self.request.GET.get('ordering')
        atLeastOne = self.request.GET.get('atLeastOne')

        qs = Drink.objects.all()

        if query:
            qs = qs.filter(name__icontains=query)
        elif filters:
            qs = qs.filter(playlist__name__iexact=filters[0])
            for filter in filters[1:]:
                qs = qs | Drink.objects.filter(
                    playlist__name__iexact=filter)

        elif user.is_authenticated and userQuery:
            qs = qs.filter(user=user)


        if not user.is_authenticated and userQuery:
            qs = Drink.objects.none()

        print('USER IS ', user)
        # if user.is_authenticated and atLeastOne:
        #     print('ATLEAST ONE')

        if not user.is_authenticated:
            user = None

        if not order:
            order = '-timestamp'

        qs = getCountedDrinks(qs, user )
        qs = qs.order_by(order)
            
        return qs
