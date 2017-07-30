from django.test import TestCase
from .utils import (
    get_channel_from_name,
    get_playlists_from_channel,
    get_all_videos_in_playlist,
    print_json
)

from .tasks import process_youtube_videos, update_all_drinks
from .models import *
from django.db.models import *


class UtilsTest(TestCase):
    # def test_query(self):
    #     qs = Drink.objects.all()
    #     qs1 = qs.annotate(count=F('ingredients'))
    #     for obj in qs1:
    #         print(obj.count)


    def test_youtube_api(self):
        # update_all_drinks()
        process_youtube_videos.delay()





