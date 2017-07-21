from django.test import TestCase
from .utils import (
    get_channel_from_name,
    get_playlists_from_channel,
    get_all_videos_in_playlist,
    print_json
)

from .tasks import process_youtube_videos

class UtilsTest(TestCase):

    def test_youtube_api(self):
        process_youtube_videos.delay()





