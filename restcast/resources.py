from django.core.urlresolvers import reverse
from djangorestframework.resources import ModelResource
from restcast.models import Podcast, Episode

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
              'content', 'link', 'id', 'listened',)
    ordering = ('-updated',)

    def podcast(self, instance):
        return reverse('podcast', kwargs={'id': instance.podcast.id})

    def listened(self, instance):
        watched_records = instance.watchedrecord_set.filter(user=self.request.user)
        return watched_records.count() > 0
