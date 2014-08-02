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
                       )