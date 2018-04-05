from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.django, name='py_django'),
    url(r'^notes$', views.notes, name='py_notes')
]
