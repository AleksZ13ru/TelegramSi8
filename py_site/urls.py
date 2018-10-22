from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.django, name='py_django'),
    url(r'^notes$', views.notes, name='py_notes'),
    url(r'^notes_b$', views.notes_b, name='py_notes_b')
]
