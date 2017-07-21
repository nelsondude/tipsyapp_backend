from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model
from django.db.models import Count

from .serializers import IngredientModelSerializer

from cocktail.api.pagination import LargeResultsSetPagination
from cocktail.models import Ingredient

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
            if obj.user.all().filter(username=user_obj.username).exists():
                obj.user.remove(user_obj)
            else:
                obj.user.add(user_obj)
            obj.save()
        return obj

class IngredientListAPIView(ListAPIView):
    serializer_class = IngredientModelSerializer
    pagination_class = LargeResultsSetPagination
    # permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('q')
        suggested = self.request.GET.get('suggested')
        qs = Ingredient.objects.all()
        if query:
            qs = Ingredient.objects.filter(name__icontains=query)
        elif suggested:
            qs = Ingredient.objects.exclude(user=user).annotate(num_drinks=Count('drink')) \
                 .order_by('-num_drinks')[:5]
        elif user.is_authenticated():
            qs = Ingredient.objects.filter(user=user).order_by('name')
        return qs

'''
queryset of all ingredients in pantry
for each drink in the website, find count of ingredients in ingredients queryset
then find intersection of all possible querysets and list counts
for ones with the highest counts, list those first


'''
