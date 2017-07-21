from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from cocktail.api.pagination import (
    LargeResultsSetPagination
)
from cocktail.models import Drink, Playlist
from .serializers import (
    DrinkListModelSerializer,
    DrinkDetailModelSerializer,
    PlaylistModelSerializer
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
    queryset = Playlist.objects.all()
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
    pagination_class = LargeResultsSetPagination
    permission_classes = [AllowAny]
    ordering_fields = ('count_need', 'timestamp', )

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = Drink.objects.all()
        userQuery = self.request.GET.get('user')
        query = self.request.GET.get("q")
        filters = self.request.GET.getlist('filter')
        if query:
            qs = qs.filter(name__icontains=query)
        elif filters:
            qs = qs.filter(playlist__name__iexact=filters[0])
            for filter in filters[1:]:
                qs = qs | Drink.objects.filter(playlist__name__iexact=filter)
        elif userQuery and user.is_authenticated():
            qs = qs.filter(user=user)
            print(qs)

        return qs.order_by('-timestamp')

#
# class PossibleDrinksAPIView(ListAPIView):
#     serializer_class = DrinkListModelSerializer
#     pagination_class = LargeResultsSetPagination
#     queryset = Drink.objects.all().order_by('-timestamp')
