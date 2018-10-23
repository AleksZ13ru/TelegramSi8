from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.django, name='py_django'),
    url(r'^notes$', views.notes, name='py_notes'),
    url(r'^notes_b$', views.notes_b, name='py_notes_b'),
    # url(r'^notes_b/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$', views.notes_b_history, name='notes_b_history'),
    path('notes_b/<int:year>/<int:month>/<int:day>/', views.notes_b_history, name='notes_b_history'),
    # url(r'^notes_b/(?P<pk>[0-9]+)/$', views.notes_detail, name='notes_detail'),


]
