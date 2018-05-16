from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    visible = models.BooleanField(default=True)
    name = models.CharField(max_length=1000)
    thumbnail = models.URLField()
    playlist_id = models.CharField(max_length=1000)
    webpage_urls = models.ManyToManyField(WebpageURL, blank=True)


    def __str__(self):
        return self.name


# ________________________________________________________________
# Ingredient Models

class Ingredient(models.Model):
    name                = models.CharField(max_length = 1000)
    ingredient_category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
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
# ________________________________________________________________
# Drink Model

class Drink(models.Model):
    name                = models.CharField(max_length = 1000, null=True, blank=True)
    webpage_url         = models.ForeignKey(WebpageURL, null=True, blank=True, on_delete=models.CASCADE)
    thumbnail           = models.URLField(null=True, blank=True)
    ingredients         = models.ManyToManyField(Ingredient, blank=True)
    slug                = models.SlugField(max_length=255, unique=True)
    timestamp           = models.DateTimeField(null=True, blank=True)
    rating              = models.FloatField(default=5)

    # User saved drinks
    user                = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    playlist            = models.ManyToManyField(Playlist, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        url = reverse("cocktail:drink") + str(self.id)
        return url

    def get_api_url(self):
        return reverse("api:drink-api:detail", kwargs={"slug": self.slug})


class Layer(models.Model):
    layer = models.CharField(max_length=1000)
    drink = models.ForeignKey(Drink, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.layer


class Amount(models.Model):
    amount              = models.CharField(max_length = 1000, null=True, blank=True)
    ingredient          = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    layer               = models.ForeignKey(Layer, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.layer.layer)+' | '+str(self.amount) + " | " + str(self.ingredient)



'''
class IngredientsUserNeeds(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    count_have = models.IntegerField(default=0)
    drinks = models.ManyToManyField(Drink)

    class Meta:
        ordering = ['-count_have']

    def __str__(self):
        return '%s | %s' % (self.user.username, self.drinks.all().count())
'''

# _____________________________________________________________
# Account Profile Extra Information


class Profile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    bio             = models.TextField(max_length=500, blank=True)
    location        = models.CharField(max_length=30, blank=True)
    birth_date      = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

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

