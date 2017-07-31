from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from cocktail.api.pagination import (
    LargeResultsSetPagination,
    StandardResultsSetPagination
)
from cocktail.models import Drink, Playlist, IngredientsUserNeeds
from .serializers import (
    DrinkListModelSerializer,
    DrinkDetailModelSerializer,
    PlaylistModelSerializer,
    DrinkCCListSerializer
)

from cocktail.tasks import process_youtube_videos, update_drink_counts

User = get_user_model()

class UpdateDatabaseAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self, request, *args, **kwargs):
        process_youtube_videos.delay()
        return Response({'updating': True}, status=200)


class PlaylistListAPIView(ListAPIView):
    serializer_class = PlaylistModelSerializer
    permission_classes = [AllowAny]
    queryset = Playlist.objects.all().order_by('name')
    pagination_class = LargeResultsSetPagination


class DrinkDetailAPIView(UpdateModelMixin, RetrieveAPIView):
    queryset = Drink.objects.all()
    serializer_class = DrinkDetailModelSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def get_object(self):
        obj = super(DrinkDetailAPIView, self).get_object()
        changeUser = self.request.GET.get('changeUser')
        qs = User.objects.filter(username=self.request.user.username)
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
    # permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        user        = self.request.user
        userQuery   = self.request.GET.get('user')
        query       = self.request.GET.get("q")
        filters     = self.request.GET.getlist('filter')
        order       = self.request.GET.get('ordering')

        if not IngredientsUserNeeds.objects.all().filter(user=user).exists():
            update_drink_counts(user)

        qs = Drink.objects.all()
        if query:
            qs = qs.filter(name__icontains=query)
        elif filters:
            print(filters)
            qs = qs.filter(playlist__name__iexact=filters[0])
            for filter in filters[1:]:
                qs = qs | Drink.objects.filter(
                    playlist__name__iexact=filter)
        elif userQuery and user.is_authenticated():
            qs = qs.filter(user=user)

        if order:
            if order == 'timestamp':
                qs = qs.order_by('-timestamp').distinct()
            else:
                qs = sorted(qs.distinct(),
                                   key= lambda obj:
                                   (obj.ingredientsuserneeds_set
                                   .all()
                                   .filter(user=user)
                                   .first()
                                   .count_need)/(obj.ingredients.all().count()),
                                   )
        return qs



class DrinkCountsAPIView(ListAPIView):
    serializer_class = DrinkCCListSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        userQuery = self.request.GET.get('user')
        query = self.request.GET.get("q")
        filters = self.request.GET.getlist('filter')
        order = self.request.GET.get('ordering')

        qs = IngredientsUserNeeds.objects.all().filter(user=user)
        if query:
            qs = qs.filter(drinks__name__icontains=query)
        elif filters:
            print(filters)
            qs = qs.filter(drinks__playlist__name__iexact=filters[0])
            for filter in filters[1:]:
                qs = qs | IngredientsUserNeeds.objects.filter(
                    drinks__playlist__name__iexact=filter)
        elif userQuery and user.is_authenticated():
            qs = qs.filter(drinks__user=user)
            for obj in qs:
                sub_qs = obj.drinks.all()
                new_qs = sub_qs.filter(user=user)
                obj.drinks = new_qs

        return qs.distinct()