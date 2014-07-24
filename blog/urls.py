__author__ = 'piratos'
from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog.views',
                       url(r'^$', 'index'),
                       url(r'^read/(?P<blog_url>\w+)/$', 'read'),
                       url(r'^read/\w+/comment/', 'add_message'),
                       )