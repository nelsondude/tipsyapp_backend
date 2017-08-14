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
        if user.is_authenticated():
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

    def get_queryset(self, *args, **kwargs):
        user        = self.request.user
        userQuery   = self.request.GET.get('user')
        query       = self.request.GET.get("q")
        filters     = self.request.GET.getlist('filter')
        order       = self.request.GET.get('ordering')
        atLeastOne  = self.request.GET.get('atLeastOne')

        if user.is_authenticated() and not IngredientsUserNeeds.objects.all().filter(user=user).exists():
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

        elif user.is_authenticated() and userQuery:
            qs = qs.filter(user=user)

        if not user.is_authenticated() and userQuery:
            qs = Drink.objects.none()

        if user.is_authenticated() and atLeastOne:
            needs_qs = IngredientsUserNeeds.objects.all().filter(user=user, count_have=0)
            if needs_qs.exists():
                needs_obj = needs_qs.first()
                qs = qs.exclude(id__in=[obj.id for obj in needs_obj.drinks.all()])

        if order:
            if order == 'timestamp':
                qs = qs.order_by('-timestamp').distinct()
            elif user.is_authenticated() and order == 'count_need':
                qs = sorted(qs.distinct(),
                                   key= lambda obj:
                                   obj.ingredients.all().count() -
                                   obj.ingredientsuserneeds_set
                                   .all()
                                   .filter(user=user)
                                   .first()
                                   .count_have
                                   )

            elif user.is_authenticated() and order == 'count_have':
                qs = sorted(qs.distinct(),
                                   key= lambda obj:
                                   obj.ingredientsuserneeds_set
                                   .all()
                                   .filter(user=user)
                                   .first()
                                   .count_have,
                                    reverse=True
                                   )
        return qs