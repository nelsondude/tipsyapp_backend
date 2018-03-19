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



from cocktail.api.pagination import (
    LargeResultsSetPagination,
    StandardResultsSetPagination
)
from cocktail.models import Drink, Playlist
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
            print('ATLEAST ONE')

        # if order:
        #     query = '''
        #                 SELECT *, count_total-count_have AS count_need, ROUND(cast(count_have as DECIMAL) / count_total, 2) AS percent
        #                 FROM (SELECT
        #                     cd.name,
        #                     cd.id AS drink_id,
        #                     COUNT(*) filter (WHERE ci.name IN (
        #                       SELECT ci.name
        #                       FROM cocktail_ingredient AS ci
        #                       JOIN cocktail_ingredient_user AS ciu ON ci.id=ciu.ingredient_id
        #                       WHERE ciu.user_id=21S
        #                     )) AS count_have,
        #                     count(*) AS count_total
        #                   FROM cocktail_drink AS cd
        #                   JOIN cocktail_drink_ingredients AS cdi ON cd.id=cdi.drink_id
        #                   JOIN cocktail_ingredient AS ci ON ci.id=cdi.ingredient_id
        #                   GROUP BA cd.name, cd.id) AS ss
        #                 ORDER BY percent DESC, count_total DESC, drink_id DESC
        #             '''
        #
        #     if order == 'timestamp':
        #         qs = qs.order_by('-timestamp').distinct()
        #     elif user.is_authenticated() and order == 'count_need':
        #         qs1 = qs.raw(query)
        #         print('count_need')
        #
        #
        #     elif user.is_authenticated() and order == 'count_have':
        #         print('count_have')
        #         pass
        #
        #     elif user.is_authenticated() and order == 'percent':
        #         print('count_percent')
        #         qs = qs.raw(query)
        #         pass
        # data = list(qs.values())
        return qs
