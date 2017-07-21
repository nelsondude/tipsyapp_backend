from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField

from django.utils.timesince import timesince

from cocktail.models import Ingredient

ingredient_detail_url = HyperlinkedIdentityField(
        view_name='api-ingredients:detail',
        lookup_field='slug'
        )


class IngredientModelSerializer(serializers.ModelSerializer):
    url = ingredient_detail_url
    number_drinks = serializers.SerializerMethodField()
    class Meta:
        model = Ingredient
        fields = [
            'url',
            'name',
            'user',
            'slug',
            'number_drinks'
        ]
    def get_number_drinks(self, obj):
        return obj.drink_set.all().count()


"""
class WebpageURLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebpageURL
        fields = [
            'webpage_url',
        ]

class AmountModelSerializer(serializers.ModelSerializer):
    ingredient = IngredientModelSerializer()
    drinks = serializers.SerializerMethodField()

    class Meta:
        model = Amount
        fields = [
            'amount',
            'ingredient',
            'drinks',
        ]

    def get_drinks(self, obj):
        qs = obj.drink_set.all()
        names = []
        for drink in qs:
            names.append(drink.name)
        return names

"""
