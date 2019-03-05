

from django.db import connection
import json


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def print_json(recipe):
    print(json.dumps(recipe, sort_keys=True, indent=4, separators=(',', ': ')))


# ########################################
from django.db.models import Count, Q, FloatField
from django.db.models.functions import Cast
from cocktail.models import Ingredient, Drink


def get_counted_drinks(queryset, user=None):
    if user:
        user_ings = Ingredient.objects.filter(user=user)
    else:
        user_ings = Ingredient.objects.filter(user__id=-1)

    total = Count('ingredients')
    count_have = Cast(Count('ingredients', filter=Q(ingredients__in=user_ings)), FloatField())
    count_need = Count('ingredients', filter=~Q(ingredients__in=user_ings))
    qs = (queryset
          .annotate(count_total=total)
          .annotate(count_have=count_have)
          .annotate(count_need=count_need)
          .annotate(percent=Cast(count_have / total, FloatField())))

    return qs
