from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .utils import getCountedDrinks



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
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        process_youtube_videos()
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
        if user.is_authenticated and changeUser:
            if obj.user.filter(id=user.id).exists():
                obj.user.remove(user)
            else:
                obj.user.add(user)
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

        # limit results based on search and playlist
        if query:
            qs = qs.filter(name__icontains=query)
        if filters:
            qs = qs.filter(playlist__name__in=filters)

        # users drinks in side menu when AUTHENTICATED
        elif user.is_authenticated and userQuery:
            qs = qs.filter(user=user)

        # users drinks in side menu when NOT AUTHENTICATED
        if not user.is_authenticated and userQuery:
            qs = Drink.objects.none()

        if not user.is_authenticated:
            user = None

        # Default ordering of drinks

        qs = getCountedDrinks(qs, user )
        if order:
            qs = qs.order_by('-' + order, '-count_total', '-timestamp')
        else:
            qs = qs.order_by('-timestamp')
            
        return qs
