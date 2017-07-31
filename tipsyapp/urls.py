"""test_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/ingredients/',   include('cocktail.api.ingredients.urls',    namespace="api-ingredients")),
    url(r'^api/drink/',         include('cocktail.api.drink.urls',          namespace="api-drink")),
    url(r'^api/webpage_url/',   include('cocktail.api.webpage_url.urls',    namespace="api-webpage_url")),
    url(r'^api/accounts/',      include('accounts.api.urls',                namespace="api-accounts")),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^.*', TemplateView.as_view(template_name="ang_home.html"), name='index')
]
