from django.core.urlresolvers import reverse
from djangorestframework.resources import ModelResource
from restcast.models import Podcast, Episode, WatchedRecord, Subscription
from restcast.forms import WatchedRecordForm, SubscriptionForm

class PodcastResource(ModelResource):
    """
    A podcast that has a title, episodes and some meta data.
    """
    model = Podcast
    fields = ('last_updated', 'publisher', 'subtitle', 'link', 'title', 
              'rights', 'author', 'email', 'summary', 
              ('episode_set', 'EpisodeResource'), 'id',)
    ordering = ('title',)    


class EpisodeResource(ModelResource):
    """
    An episode associated with a podcast.
    """
    model = Episode
    fields = ('podcast', 'subtitle', 'title', 'author', 'updated', 'summary',
              'content', 'link', 'id', 'listened_to',)
    ordering = ('-updated',)

    def podcast(self, instance):
        return reverse('podcast', kwargs={'id': instance.podcast.id})

    def listened_to(self, instance):
        watched_records = instance.watchedrecord_set.filter(user=self.request.user)
        return watched_records.count() > 0


class WatchedRecordResource(ModelResource):
    """
    An episode associated with a podcast.
    """
    form = WatchedRecordForm
    model = WatchedRecord
    fields = ('watched', 'episode_link', 'episode_id')
    
    ordering = ('-episode',)
    
    def episode_id(self, instance):
        return instance.episode.id

    def episode_link(self, instance):
        return reverse('episode', kwargs= {'id': instance.episode.id,
                                           'podcast': instance.episode.podcast.id})


class SubscriptionResource(ModelResource):
    """
    An subscription to a podcast.
    """
    form = SubscriptionForm
    model = Subscription
    fields = ('podcast_link',)
    
    def podcast_link(self, instance):
        return instance.podcast.get_absolute_url()
