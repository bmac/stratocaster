from django.conf.urls.defaults import patterns, include, url
from restcast.views import import_podcast, EpisodeInstanceView
from djangorestframework.views import ListModelView, ModelView
from restcast.resources import PodcastResource, EpisodeResource

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
    url(r'^$', import_podcast),
    url(r'^resources/podcast/$', ListModelView.as_view(resource=PodcastResource), 
        name='podcast-root'),
    url(r'^resources/podcast/(?P<podcast_id>[^/]+)/episode/(?P<episode_id>[^/]+)/$', 
        EpisodeInstanceView.as_view(), name='episode'),
    url(r'^resources/podcast/(?P<podcast_id>[^/]+)/$', 
        ModelView.as_view(resource=PodcastResource), name='podcast'),
    url(r'^resources/podcast/(?P<podcast_id>[^/]+)/episode/$', 
       ListModelView.as_view(resource=EpisodeResource), name='episode-root'),


)
