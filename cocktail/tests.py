from django.test import TestCase
from .utils import (
    get_channel_from_name,
    get_playlists_from_channel,
    get_all_videos_in_playlist,
    print_json
)

from .tasks import process_youtube_videos
from .models import *
from django.db.models import *


class UtilsTest(TestCase):

    def test_querying(self):
        user_ings = Ingredient.objects.filter(user__id=1)
        totals_qs = Drink.objects.annotate(count_total=Count('ingredients'))
        count_have = Drink.objects.filter(ingredients__in=user_ings).annotate(count_have=Count('ingredients'))
        print(user_ings[0])
        print(count_have[0])

    # def test_youtube_api(self):
    #     process_youtube_videos()





