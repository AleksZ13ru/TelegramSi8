from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.django, name='py_django'),
    url(r'^notes$', views.notes_b, name='py_notes_b'),
    url(r'^report$', views.report, name='py_report_b'),
    path('notes_b/<int:year>/<int:month>/<int:day>/', views.notes_b_history, name='notes_b_history'),
    # path('report$/<int:year>/<int:month>/<int:day>/', views.report_history, name='report_history'),

    path('filter/<int:filter>/party/<int:party>/date/<int:year>/<int:month>/<int:day>/', views.machine_filter,
         name='filter'),
    path('report/filter/<int:filter>/party/<int:party>/date/<int:year>/<int:month>/<int:day>/',
         views.report_history, name='report_history')

    # url(r'^notes_b/(?P<pk>[0-9]+)/$', views.notes_detail, name='notes_detail'),

    # логика ссылок нужно

]
