

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

def getDrinks(order):
    if order == 'percent':
        sqlOrder = 'order by percent desc, count_total desc, drink_id desc'
    elif order == 'count_have':
        sqlOrder = 'order by count_have desc, count_total, drink_id desc'
    elif order == 'count_need':
        sqlOrder = 'order by count_need, count_total desc, drink_id desc'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT *, count_total-count_have AS count_need, ROUND(cast(count_have as DECIMAL) / count_total, 2) AS percent
            FROM (SELECT
                cd.name,
                cd.id AS drink_id,
                COUNT(*) filter (WHERE ci.name IN (
                  SELECT ci.name
                  FROM cocktail_ingredient AS ci
                  JOIN cocktail_ingredient_user AS ciu ON ci.id=ciu.ingredient_id
                  WHERE ciu.user_id=21
                )) AS count_have,
                count(*) AS count_total
              FROM cocktail_drink AS cd
              JOIN cocktail_drink_ingredients AS cdi ON cd.id=cdi.drink_id
              JOIN cocktail_ingredient AS ci ON ci.id=cdi.ingredient_id
              GROUP BY cd.name, cd.id) AS ss
            order by percent desc, count_total desc, drink_id desc
            LIMIT 2
        """)
        rows = dictfetchall(cursor)

    # print_json(rows)
    print(rows)
    return rows