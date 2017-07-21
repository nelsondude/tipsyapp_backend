import nltk
import string
import copy

import json
import urllib.parse
import urllib.request
import requests
import datetime

from nltk import word_tokenize
from langdetect import detect

from .models import Drink


def myDeepCopy(a):
    if (isinstance(a, list) or isinstance(a, tuple)):
        return [myDeepCopy(element) for element in a]
    else:
        return copy.copy(a)



def print_json(recipe):
    print(json.dumps(recipe, sort_keys=True, indent=4, separators=(',', ': ')))


class DescriptionLineDetails(object):
    def __init__(self, line, contain_title, proper_nouns, num_key_words, banned, is_layer):
        self.line           = line
        self.contain_title  = contain_title
        self.proper_nouns   = proper_nouns
        self.num_key_words  = num_key_words
        self.banned         = banned
        self.is_layer       = is_layer

def seperate_amount_from_ingredient(line):
    key_words = "of ) cup dashes drops cups oz oz. ml ml. pack with teaspoon tsp tablespoon tbsp part bottle bottles gal. gallon pint dash pinch splash".split(" ")
    latest_index = 0
    words = line.split(" ")
    for i in range(len(words)):
        word = words[i]
        for j in range(len(key_words)):
            key_word = key_words[j]
            if word.lower().endswith(key_word) or (len(word)>0 and word[-1] in string.digits):
                latest_index = i + 1

    amount = " ".join(words[:latest_index])
    ingredient = " ".join(words[latest_index:])
    result = [amount, ingredient.strip()]

    return result

def filter_recipe(recipe):
    return (len(recipe['title'])>2 and
            len(recipe['layers'])>0 and
            len(recipe['layers'][0]['ingredients'])>1 and
            len(recipe['title'].split(" "))<7)


def get_ingredients_from_description(description, title):
    chunks = get_description_chunks(description, title)
    detailed_info = score_chunks(chunks)
    recipes = []
    recipe =    {
                    "title": "",
                    "layers": [],
                    "language": "",
                    "layer": False
                }

    title = ""
    for i in range(len(detailed_info)):
        chunk, score, layer = detailed_info[i]

        lang = ""
        if score > 2:
            current_layer = {
                                "layer_title": layer,
                                "ingredients": [],
                            }
            for j in range(len(chunk)):
                obj = chunk[j]
                if j == 0 and "layer" not in obj.line.lower():
                    title = obj.line.title()
                    lang = detect(obj.line.title())

                if j != 0 and "layer" not in obj.line.lower():
                    line = myDeepCopy(seperate_amount_from_ingredient(obj.line))
                    if len(line[1])>0 and "=" not in line[1]:
                        current_layer["ingredients"].append(line)

            if len(recipe['title'])==0:
                recipe['title'] = title

            if len(title)>0 and title != recipe['title']:
                if filter_recipe(recipe):
                    recipes.append(recipe)

                my_new_recipe = {
                    "title": title,
                    "layers": [],
                    "language": "",
                    "layer": False
                }

                recipe = my_new_recipe


            recipe['layers'].append(current_layer)

    if filter_recipe(recipe):
        recipes.append(recipe)
    return recipes


def get_description_chunks(description, title):
    chunks = []
    current_chunk = []
    lines = description.splitlines()
    i = 0
    key_words = "layer splash part oz ml tequila rum vodka gin liqueur grenadine"
    banned_words = "find instagram angeles @ http contact email vlog channel outtakes preparation"
    for line in description.splitlines():

        contain_title = True if title.lower() in line.lower() else False
        text          = word_tokenize(line)
        tagged        = nltk.pos_tag(text)
        proper_nouns  = 0
        num_key_words = 0
        banned        = False
        is_layer      = True if "layer" in line.lower() else False

        for word, tag in tagged:
            if tag.startswith("NN"): proper_nouns += 1

        for key_word in key_words.split(" "):
            if key_word in line.lower(): num_key_words += 1

        for banned_word in banned_words.split(" "):
            if banned_word in line.lower(): banned = True

        details = DescriptionLineDetails(
                            line,
                            contain_title,
                            proper_nouns,
                            num_key_words,
                            banned,
                            is_layer,
                            )

        if ((i == 0) or (len(current_chunk[i-1].line)==0 and len(line)!=0)):
            chunks.append(current_chunk)
            current_chunk = []
            i = 0

        current_chunk.append(details)
        i += 1

    result = myDeepCopy(chunks)
    return result

def score_chunks(chunks):
    # scores = []
    detailed_info = []
    for chunk in chunks:
        layer = ""
        score = 0
        words = 0
        # title = ""

        for obj in chunk:
            if len(obj.line.strip()) == 0: #remove all empty lines in a chunk
                chunk.remove(obj)
                continue

            if obj.is_layer:
                layer = obj.line

            # if i == 0 and "layer" not in obj.line.lower():
            #     title = obj.line.title()

            line = obj.line
            words += len(obj.line.split(" "))
            score += obj.proper_nouns * 3 #weight for properNOUN
            score += obj.num_key_words * 15 #weight for keywords
            if obj.contain_title: score += 30 #weight for Title
            if obj.banned: #if any banned words, score is 0
                score = 0
                break

        if words > 0 and score > 0: score = score/words #score per word
        if len(chunk) < 2: score = 0

        detailed_info.append([chunk, score, layer])

    result = myDeepCopy(detailed_info)
    return result


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
    ids = []
    for item in data['items']:
        id = item['id']
        ids.append(id)
    return ids


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
    if not videos: videos = []
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    publishedAfter = '1970-01-01T00:00:00Z'
    qs = Drink.objects.all().order_by('-timestamp')
    publishedBefore = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")+"Z"
    if qs.exists():
        publishedAfter = qs.first().timestamp.strftime("%Y-%m-%dT%H:%M:%S")+"Z"

    values = {
        'part': 'snippet',
        'playlistId': playlist.get('id'),
        'maxResults': 50,
        'publishedAfter': publishedAfter,
        'publishedBefore': publishedBefore
    }
    if nextPageToken:
        values['pageToken'] = nextPageToken

    data = get_json(url, values)
    nextPageToken = data.get('nextPageToken')
    for item in data['items']:
        title = item['snippet']['title']
        description = item['snippet']['description']
        recipes = get_ingredients_from_description(description, title)
        video_id = item['snippet']['resourceId']['videoId']
        youtube_link = "https://www.youtube.com/watch?v="+video_id
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
    channel_id = get_channel_from_name('TipsyBartender')[0]
    playlists = get_playlists_from_channel(channel_id)
    result = []
    for playlist in playlists:
        print("NEW PLAYLIST")
        videos = get_all_videos_in_playlist(playlist)
        result.extend(videos)
    return result
