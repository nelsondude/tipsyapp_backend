

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

def getDrinks(order, userId=-1):
    sqlOrder = [userId, 'timestamp DESC', 'DESC']
    if order == 'percent':
        sqlOrder = [userId, 'percent DESC', 'DESC']
    elif order == 'count_have':
        sqlOrder = [userId, 'count_have DESC', '']
    elif order == 'count_need':
        sqlOrder = [userId, 'count_need', 'DESC']

    qs = """
          SELECT name, count_have, count_total, slug, thumbnail FROM
            (SELECT DISTINCT *, count_total-count_have AS count_need, ROUND(cast(count_have as DECIMAL) / count_total, 2) AS percent
              FROM (SELECT
                  cd.timestamp,
                  cd.thumbnail,
                  cd.name,
                  cd.slug,
                  cd.id AS drink_id,
                  COUNT(*) filter (WHERE ci.name IN (
                    SELECT ci.name
                    FROM cocktail_ingredient AS ci
                    JOIN cocktail_ingredient_user AS ciu ON ci.id=ciu.ingredient_id
                    WHERE ciu.user_id=%s
                  )) AS count_have,
                  count(*) AS count_total
                FROM cocktail_drink AS cd
                JOIN cocktail_drink_ingredients AS cdi ON cd.id=cdi.drink_id
                JOIN cocktail_ingredient AS ci ON ci.id=cdi.ingredient_id
                GROUP BY cd.name, cd.id) AS ss
              ORDER BY %s, count_total %s, drink_id DESC
              LIMIT 16) AS sss
        """ % tuple(sqlOrder)

    with connection.cursor() as cursor:
        cursor.execute(qs)
        rows = dictfetchall(cursor)

    return rows



# ########################################
from django.db.models import Count, Q, FloatField
from django.db.models.functions import Cast
from cocktail.models import Ingredient, Drink


def getCountedDrinks(queryset, user=None):
    if user:
        user_ings = Ingredient.objects.filter(user=user)
    else:
        user_ings = Ingredient.objects.filter(user__id=-1)

    total = Count('ingredients')
    count_have = Cast(Count('ingredients', filter = Q(ingredients__in=user_ings)), FloatField())
    count_need = Count('ingredients', filter = ~Q(ingredients__in=user_ings))
    qs = (queryset
        .annotate(count_total=total)
        .annotate(count_have=count_have)
        .annotate(count_need=count_need)
        .annotate(percent=Cast(count_have/total, FloatField())))

    return qs