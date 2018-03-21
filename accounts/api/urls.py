from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

from rest_framework_jwt.views import obtain_jwt_token

from .views import RegisterAPIView, LoginAPIView, UserAPIView

app_name="accounts"

urlpatterns = [
    url(r'^register/$', RegisterAPIView.as_view(), name='register'),
    url(r'^login/token/', obtain_jwt_token),
    url(r'^$', UserAPIView.as_view(), name='user')

]
