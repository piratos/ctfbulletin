from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', include('challenges.urls')),
                       url(r'^talk/', include('talk.urls')),
                       url(r'^blog/', include('blog.urls')),
                       url(r'challenges/', include('challenges.urls')),
                       url(r'ctf/', include('ctf.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )