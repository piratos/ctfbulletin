from django.conf.urls import patterns, url

urlpatterns = patterns('talk.views',

                       url(r'^index/$', 'index'),
                       url(r'^category/(?P<cat_name>\w+)/$', 'category'),  # display threads of chosen challengecategory
                       url(r'^category/\w+/(?P<thread_id>\d+)/$', 'thread'),  # display message of a thread
                       url(r'add_message/', 'add_message'),  # adding message in a thread
                       )