# -*- coding: utf8 -*-

from django.conf.urls import url

from .views import CommandReceiveView
from . import views

app_name = 'viber'

urlpatterns = [
    # url(r'^bot$', CommandReceiveView.as_view(), name='command'),
    url(r'^$', CommandReceiveView.as_view(), name='command'),
    # url(r'^$', views.django, name='planet_django')
]
