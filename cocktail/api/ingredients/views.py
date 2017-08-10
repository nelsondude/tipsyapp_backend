from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model
from django.db.models import Count

from .serializers import IngredientModelSerializer

from cocktail.api.pagination import LargeResultsSetPagination
from cocktail.models import Ingredient
from cocktail.tasks import update_drink_counts

User = get_user_model()


class IngredientDetailAPIView(UpdateModelMixin, RetrieveAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientModelSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def get_object(self):
        obj = super(IngredientDetailAPIView, self).get_object()
        qs = User.objects.filter(username=self.request.user.username)
        if qs.exists() and qs.count() == 1:
            user_obj = qs.first()
            added = True
            if obj.user.all().filter(username=user_obj.username).exists():
                obj.user.remove(user_obj)
                added = False
            else:
                obj.user.add(user_obj)
            obj.save()
            update_drink_counts(user_obj, ingredient=obj)
        return obj

class IngredientListAPIView(ListAPIView):
    serializer_class = IngredientModelSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('q')
        suggested = self.request.GET.get('suggested')
        if query:
            qs = Ingredient.objects.filter(name__icontains=query)
        elif suggested:
            if user.is_authenticated():
                qs = Ingredient.objects.exclude(user=user).annotate(num_drinks=Count('drink')) \
                 .order_by('-num_drinks')[:15]
            else:
                qs = Ingredient.objects.annotate(num_drinks=Count('drink')) \
                 .order_by('-num_drinks')[:15]
        elif user.is_authenticated():
            qs = Ingredient.objects.filter(user=user).order_by('name')
        else:
            qs = Ingredient.objects.none()
        return qs

