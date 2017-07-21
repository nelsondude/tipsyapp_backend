from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model

User = get_user_model()

# ________________________________________________________________
# Miscellaneous Models

class WebpageURL(models.Model):
    webpage_url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.webpage_url



class Category(models.Model):
    category = models.CharField(max_length = 1000)

    def __str__(self):
        return self.category

class Playlist(models.Model):
    name = models.CharField(max_length=1000)
    thumbnail = models.URLField()
    playlist_id = models.CharField(max_length=1000)


    def __str__(self):
        return self.name


# ________________________________________________________________
# Ingredient Models

class Layer(models.Model):
    layer = models.CharField(max_length=1000)

    def __str__(self):
        return self.layer


class Ingredient(models.Model):
    name                = models.CharField(max_length = 1000)
    ingredient_category = models.ForeignKey(Category, null=True, blank=True)
    slug                = models.SlugField(max_length=255, unique=True)
    user                = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.name

    def as_dict(self):
        return {"name":self.name}

    class Meta:
        ordering = ['id']


    def get_api_url(self):
        return reverse("api:ingredients-api:detail", kwargs={"slug": self.slug})

class Amount(models.Model):
    amount              = models.CharField(max_length = 1000, null=True, blank=True)
    ingredient          = models.ForeignKey(Ingredient)
    layer               = models.ForeignKey(Layer, null=True, blank=True)


    def __str__(self):
        return str(self.amount) + " | " + str(self.ingredient)


# ________________________________________________________________
# Drink Model

class DrinkManager(models.Manager):
    def get_count_need(self, user, obj):
        ingredient_qs = obj.ingredients.all()
        user = self.context['request'].user
        user_qs = User.objects.filter(username=user.username)
        if user_qs.exists() and user_qs.count() == 1:
            user_obj = user_qs.first()
            qs = user_obj.ingredient_set.all()
            return ingredient_qs.count() - (qs & ingredient_qs).count()
        return 0

class Drink(models.Model):
    name                = models.CharField(max_length = 1000, null=True, blank=True)
    webpage_url         = models.ForeignKey(WebpageURL, null=True, blank=True)
    thumbnail           = models.URLField(null=True, blank=True)
    amount              = models.ManyToManyField(Amount, blank=True)
    ingredients         = models.ManyToManyField(Ingredient, blank=True)
    slug                = models.SlugField(max_length=255, unique=True)
    timestamp           = models.DateTimeField(null=True, blank=True)
    rating              = models.FloatField(default=5)
    user                = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    playlist            = models.ManyToManyField(Playlist, blank=True)

    # To Change: Drink has layers which have amount ingredients

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        url = reverse("cocktail:drink") + str(self.id)
        return url

    def get_api_url(self):
        return reverse("api:drink-api:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ['id']



# ________________________________________________________________
# Slug Creater for Drink and Ingredients Below

def create_slug(instance, sender, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = sender.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, sender, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance, sender)

pre_save.connect(pre_save_post_receiver, sender=Drink)
pre_save.connect(pre_save_post_receiver, sender=Ingredient)


