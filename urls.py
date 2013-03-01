from django.conf.urls.defaults import patterns, include, url
from restcast.rest_views import ReadModelView,  PodcastListView
from restcast.views import update_watched_record
from restcast.resources import PodcastResource
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stratocaster.views.home', name='home'),
    # url(r'^stratocaster/', include('stratocaster.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^resources/podcast/(?P<podcast_id>[^/]+)/episode/(?P<episode_id>[^/]+)/listened/$', 
        update_watched_record, name='listened'),
    url(r'^resources/podcast/(?P<id>[^/]+)/$', 
        ReadModelView.as_view(resource=PodcastResource), name='podcast'),
    url(r'^resources/podcast/$', PodcastListView.as_view(), 
        name='podcast-root'),
    url(r'^restframework/', include('djangorestframework.urls', namespace='djangorestframework')),
    (r'^(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/bmac/code/stratocaster/static/'}),
)
