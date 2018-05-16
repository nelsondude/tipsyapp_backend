import nltk
import json
import urllib.parse
import urllib.request
import requests

from .models import Drink, Playlist
from .recipe import get_ingredients_from_description



def print_json(recipe):
    print(json.dumps(recipe, sort_keys=True, indent=4, separators=(',', ': ')))


def get_json(url, values):
    values['key'] = 'AIzaSyAOnOiQQbBPfAg6Hlr-zl8dsmvWUOGCuHs'
    url_values = urllib.parse.urlencode(values)
    full_url = url + '?' + url_values
    return requests.get(full_url).json()


def get_channel_from_name(name):
    values = {'part': 'contentDetails',
              'forUsername': name,
              'maxResults': '50'}

    url = "https://www.googleapis.com/youtube/v3/channels"
    data = get_json(url, values)
    item = data['items'][0]
    id = item['id']
    uploaded = item['contentDetails']['relatedPlaylists']['uploads']

    return (id, uploaded)


def get_playlists_from_channel(id, nextPageToken=None, playlists=None):
    if not playlists: playlists = []
    url = "https://www.googleapis.com/youtube/v3/playlists"
    values = {
        'part': 'snippet',
        'channelId': id,
        'maxResults': 50
    }
    if nextPageToken:
        values['pageToken'] = nextPageToken
    data = get_json(url, values)
    nextPageToken = data.get('nextPageToken')

    for item in data['items']:
        info = {
            'id': item['id'],
            'title': item['snippet']['title'],
            'default_thumbnail': item['snippet']['thumbnails']['default']['url']
        }
        playlists.append(info)

    if nextPageToken:
        get_playlists_from_channel(id, nextPageToken, playlists)

    return playlists


def get_all_videos_in_playlist(playlist, nextPageToken=None, videos=None):
    if not videos:
        videos = []

    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    values = {
        'part': 'snippet, contentDetails',
        'playlistId': playlist.get('id'),
        'maxResults': 50,
        # 'publishedAfter': publishedAfter,
        # 'publishedBefore': publishedBefore
    }
    if nextPageToken:
        values['pageToken'] = nextPageToken

    data = get_json(url, values)

    # Prevent Playlists from fetching data if no new videos have been added
    count = data['pageInfo']['totalResults']
    qs = Playlist.objects.all().filter(playlist_id=playlist['id'])
    if qs.count() == 1 and videos == []:
        obj = qs.first()
        qs_count = obj.webpage_urls.all().count()
        print(qs_count, count)
        if qs_count == count:
            return videos

    # Recursive function to go through all pages until the end
    nextPageToken = data.get('nextPageToken')
    for item in data['items']:
        title = item['snippet']['title']
        description = item['snippet']['description']
        recipes = get_ingredients_from_description(description, title)
        video_id = item['snippet']['resourceId']['videoId']
        youtube_link = "https://www.youtube.com/watch?v="+video_id
        try:
            published_at = item['contentDetails']['videoPublishedAt']
        except:
            published_at = item['snippet']['publishedAt']


        try:
            thumbnail = item['snippet']['thumbnails']['maxres']['url']
        except:
            try:
                thumbnail = item['snippet']['thumbnails']['default']['url']
            except:
                thumbnail = ""

        data = {
            'webpage_url': youtube_link,
            'thumbnail': thumbnail,
            'upload': published_at,
            'playlist': playlist,
            'description': description,
            'recipes': recipes
        }
        videos.append(data)
    if nextPageToken:
        get_all_videos_in_playlist(playlist, nextPageToken, videos)

    return videos


def save_all_channel_links():
    channel_id, uploaded = get_channel_from_name('TipsyBartender')
    playlists = get_playlists_from_channel(channel_id)
    playlists.append({
        'id': uploaded,
        'title': 'Uploaded',
        'default_thumbnail': 'https://cdn1.iconfinder.com/data/icons/web-items/24/143-256.png'
    })

    result = []
    for playlist in playlists:
        print("Playlist: %s" % playlist['title'])
        videos = get_all_videos_in_playlist(playlist)
        result.extend(videos)
    return result
