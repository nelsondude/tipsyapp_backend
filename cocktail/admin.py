from django.contrib import admin

# Register your models here.

from .models import (
    Category,
    Ingredient,
    Drink,
    WebpageURL,
    Amount,
    Playlist,
    Profile
    )

admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Drink)
admin.site.register(WebpageURL)
admin.site.register(Amount)
admin.site.register(Playlist)
admin.site.register(Profile)

