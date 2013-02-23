from django.conf.urls.defaults import patterns, include, url
from djangorestframework.views import ListModelView, ModelView, InstanceModelView
from restcast.views import ReadModelView, WatchedRecordListView, PodcastListView, ReadUpdateUserModelView, SubscriptionListView, update_watched_record
from restcast.resources import PodcastResource, EpisodeResource, WatchedRecordResource, SubscriptionResource
import settings
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
    url(r'^resources/podcast/(?P<podcast>[^/]+)/episode/(?P<id>[^/]+)/$', 
        ReadModelView.as_view(resource=EpisodeResource), name='episode'),
    url(r'^resources/podcast/(?P<podcast>[^/]+)/episode/$', 
       ListModelView.as_view(resource=EpisodeResource), name='episode-root'),
    url(r'^resources/podcast/(?P<id>[^/]+)/$', 
        ReadModelView.as_view(resource=PodcastResource), name='podcast'),
    url(r'^resources/podcast/$', PodcastListView.as_view(), 
        name='podcast-root'),
    url(r'^resources/watched/(?P<pk>[^/]+)/$', ReadUpdateUserModelView.as_view(resource=WatchedRecordResource),
        name='watched-record'),
    url(r'^resources/watched/$', WatchedRecordListView.as_view()),
    url(r'^resources/subscription/$', SubscriptionListView.as_view()),
    url(r'^resources/subscription/(?P<pk>[^/]+)/$', ReadUpdateUserModelView.as_view(resource=SubscriptionResource),
        name='subscription'),    
    (r'^(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/bmac/code/stratocaster/static/'}),
)





