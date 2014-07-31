__author__ = 'piratos'
from django.conf.urls import url, patterns

urlpatterns = patterns('ctf.views',
                       url(r'^add/', 'add_team'),
                       url(r'^$', 'index'),
                       url(r'join/', 'join_team'),
                       )