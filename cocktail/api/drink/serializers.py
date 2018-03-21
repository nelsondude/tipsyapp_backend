from rest_framework import serializers, pagination
from rest_framework.relations import HyperlinkedIdentityField

from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from cocktail.models import (
    Drink,
    Amount,
    WebpageURL,
    Playlist,
    Ingredient,
    Layer
)

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
    need_it = serializers.SerializerMethodField()
    class Meta:
        model = Amount
        fields = [
            'name',
            'amount',
            'need_it'
        ]
    def get_name(self, obj):
        return obj.ingredient.name

    def get_need_it(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            qs = Ingredient.objects.filter(user=user, slug=obj.ingredient.slug)
            return not qs.exists()
        return True

class LayerModelSerializer(serializers.ModelSerializer):
    ingredients = AmountModelSerializer(many=True, source='amount_set')
    name = serializers.CharField(source='layer')
    class Meta:
        model = Layer
        fields = [
            'name',
            'ingredients'
        ]

class DrinkDetailModelSerializer(serializers.ModelSerializer):
    embed_url = serializers.SerializerMethodField()
    url = drink_detail_url
    playlists = serializers.SerializerMethodField()
    webpage_url = WebpageURLMdelSerializer()
    layers = LayerModelSerializer(many=True, source='layer_set')
    timestamp = serializers.DateTimeField(format="%b %d, %Y")

    have_it = serializers.SerializerMethodField()

    class Meta:
        model = Drink
        fields = [
            'name',
            'embed_url',
            'webpage_url',
            'thumbnail',
            'timestamp',
            'rating',
            'playlists',
            'url',
            'layers',
            'have_it'
        ]
    def get_have_it(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Drink.objects.all().filter(id=obj.id, user=user).exists()
        return False

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



class DrinkListModelSerializer(serializers.ModelSerializer):
    url = drink_detail_url

    count_need = serializers.IntegerField()
    count_have = serializers.IntegerField()
    count_total = serializers.IntegerField()
    percent = serializers.FloatField()

    class Meta:
        model = Drink
        fields = [
            'name',
            'thumbnail',
            'url',
            'count_need',
            'count_have',
            'count_total',
            'percent',
            'slug',
            'timestamp'
        ]