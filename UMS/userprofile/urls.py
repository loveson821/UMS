from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', profileDetail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/edit$', profileEdit.as_view(), name='edit'),

    # # ex: /polls/5/
    # url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)