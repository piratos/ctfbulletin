__author__ = 'piratos'
from django.conf.urls import patterns, url

urlpatterns = patterns('challenges.views',
                       url(r'^$', 'index'),
                       url(r'login/$', 'user_login'),
                       url(r'logout/$', 'user_logout'),
                       url(r'register/$', 'register'),
                       url(r'get/(?P<ch_id>\d+)', 'get_challenge'),
                       url(r'check/', 'check_flag'),
                       url(r'profile/', 'profile'),
                       url(r'^writeups/(?P<chid>\d+)/$', 'get_writeup'),
                       url(r'^writeups/\d+/(?P<wid>\d+)/$', 'full_writeup'),
                       )