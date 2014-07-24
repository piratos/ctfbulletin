__author__ = 'piratos'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('challenges.views',
                       url(r'^$', 'index'),
                       url(r'login/$', 'user_login'),
                       url(r'logout/$', 'user_logout'),
                       url(r'register/$', 'register'),
                       )