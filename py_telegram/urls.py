# -*- coding: utf8 -*-

from django.conf.urls import url

from .views import CommandReceiveView
from . import views

app_name = 'planet'

urlpatterns = [
    url(r'^bot/(?P<bot_token>.+)/$', CommandReceiveView.as_view(), name='command'),
    url(r'^$', views.django, name='planet_django')
]
