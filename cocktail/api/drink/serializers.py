from rest_framework import serializers, pagination
from rest_framework.relations import HyperlinkedIdentityField

from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from cocktail.models import Drink, Amount, WebpageURL, Playlist, IngredientsUserNeeds

import urllib.parse as urlparse

User = get_user_model()

drink_detail_url = HyperlinkedIdentityField(
        view_name='api-drink:detail',
        lookup_field='slug'
        )

class PlaylistModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = [
            'name',
        ]

class WebpageURLMdelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebpageURL
        fields = [
            'webpage_url',
            'description'
        ]

class AmountModelSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Amount
        fields = [
            'name',
            'amount',
        ]
    def get_name(self, obj):
        return obj.ingredient.name

class DrinkDetailModelSerializer(serializers.ModelSerializer):
    amount = AmountModelSerializer(many=True)
    count_need = serializers.SerializerMethodField()
    embed_url = serializers.SerializerMethodField()
    url = drink_detail_url
    playlists = serializers.SerializerMethodField()
    webpage_url = WebpageURLMdelSerializer()

    class Meta:
        model = Drink
        fields = [
            'name',
            'embed_url',
            'webpage_url',
            'count_need',
            'thumbnail',
            'amount',
            'timestamp',
            'rating',
            'playlists',
            'url',
            'user',
        ]

    def get_playlists(self, obj):
        result = []
        for playlist in obj.playlist.all():
            result.append(playlist.name)
        return result

    def get_embed_url(self, obj):
        url = obj.webpage_url.webpage_url
        embed = urlparse.parse_qs(urlparse.urlparse(url).query).get('v')[0]
        pre = "https://www.youtube.com/embed/"
        return pre + embed

    def get_count_need(self, obj):
        ingredient_qs = obj.ingredients.all()
        user = self.context['request'].user
        user_qs = User.objects.filter(username=user.username)
        if user_qs.exists() and user_qs.count() == 1:
            user_obj = user_qs.first()
            qs = user_obj.ingredient_set.all()
            return ingredient_qs.count() - (qs & ingredient_qs).count()
        return 0


class DrinkListModelSerializer(serializers.ModelSerializer):
    url = drink_detail_url
    count_need = serializers.SerializerMethodField()
    class Meta:
        model = Drink
        fields = [
            'name',
            'thumbnail',
            'url',
            'count_need',
            'slug'
        ]
    def get_count_need(self, obj):
        count_obj = obj.ingredientsuserneeds_set.all().filter(user=self.context['request'].user).first()
        if count_obj:
            return count_obj.count_need
        return obj.ingredients.all().count()


class DrinkCCListSerializer(serializers.HyperlinkedModelSerializer):
    drinks = serializers.SerializerMethodField('paginated_drinks')
    class Meta:
        model = IngredientsUserNeeds
        fields = [
            'count_need',
            'user',
            'drinks'
        ]
    def paginated_drinks(self, obj):
        drinks = Drink.objects.filter(ingredientsuserneeds=obj)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(drinks, self.context['request'])
        serializer = DrinkListModelSerializer(page, many=True, context={'request': self.context['request']})
        return serializer.data
