from __future__ import absolute_import, unicode_literals

import dateutil.parser
from datetime import date
from celery.decorators import task
from .utils import (
    get_channel_from_name,
    get_playlists_from_channel,
    get_all_videos_in_playlist,
    save_all_channel_links
)
from .models import (
    Ingredient,
    Drink,
    WebpageURL,
    Amount,
    Layer,
    Playlist
)

@task(name="process_videos")
def process_youtube_videos():
    # channel_id = get_channel_from_name('TipsyBartender')[0]
    # playlists = get_playlists_from_channel(channel_id)
    # entries = get_all_videos_in_playlist(playlists[0])
    entries = save_all_channel_links()
    for i in range(len(entries)):
        print(i*100/len(entries))
        entry_dict = entries[i]
        url                  = entry_dict.get("webpage_url")
        thumbnail            = entry_dict.get("thumbnail")
        playlist             = entry_dict.get("playlist")
        description          = entry_dict.get("description")
        upload               = dateutil.parser.parse(entry_dict.get("upload"))

        webpage_obj, created = WebpageURL.objects.get_or_create(
            webpage_url=url,
            description=description)
        if not created:
            webpage_obj.save()

        playlist_obj, created = Playlist.objects.get_or_create(
            name=playlist['title'].title(),
            thumbnail=playlist['default_thumbnail'],
            playlist_id=playlist['id'])

        if not created:
            playlist_obj.save()

        for recipe in entry_dict.get("recipes"):
            name = recipe.get("title").title().strip()
            drink, created = Drink.objects.get_or_create(
                                            name=name,
                                            webpage_url=webpage_obj,
                                            thumbnail=thumbnail,
                                            timestamp=upload
                                            )
            if created:
                drink.save()
                for layer in recipe.get("layers"):
                    layer_title = layer.get("layer_title").title()
                    layer_title_obj = Layer(layer=layer_title)
                    layer_title_obj.save()
                    for amount, ingredient in layer["ingredients"]:
                        ingredient_obj, created = Ingredient.objects.get_or_create(name=ingredient.title().strip())
                        if created:
                            ingredient_obj.save()

                        ingred_amount_obj = Amount(
                                            amount=amount,
                                            ingredient=ingredient_obj,
                                            layer=layer_title_obj
                                            )
                        ingred_amount_obj.save()
                        drink.amount.add(ingred_amount_obj)
                        drink.ingredients.add(ingredient_obj)
            drink.playlist.add(playlist_obj)
