from rest_framework import serializers
from django.utils.timesince import timesince

from cocktail.models import Drink, Ingredient, Amount, WebpageURL

class IngredientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'name',
        ]

class AmountModelSerializer(serializers.ModelSerializer):
    ingredient = IngredientModelSerializer()
    
    class Meta:
        model = Amount
        fields = [
            'ingredient',
        ]



class DrinkModelSerializer(serializers.ModelSerializer):
    # amount_ingredients = AmountModelSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Drink
        fields = [
            'name',
            'ingredients',
            'thumbnail',
        ]

    def get_ingredients(self, obj):
        qs = obj.amount_ingredients.all()
        result = []
        for ingredient_obj in qs:
            result.append(ingredient_obj.ingredient.name)
        return result


class WebpageURLModelSerializer(serializers.ModelSerializer):
    drink_set = DrinkModelSerializer(many=True)


    class Meta:
        model = WebpageURL
        fields = [
            'webpage_url',
            'drink_set',
        ]

