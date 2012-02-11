from django.core.urlresolvers import reverse
from djangorestframework.resources import ModelResource
from restcast.models import Podcast, Episode


class PodcastResource(ModelResource):
    """
    A podcast that has a title, episodes and some meta data.
    """
    model = Podcast
    fields = ('last_updated', 'version', 'publisher', 'subtitle', 'link', 'title', 
              'rights', 'author', 'email', 'summary', 'episodes', 
              'id',)
    ordering = ('title',)

    def episodes(self, instance):
        ret = []
        for episode in instance.episode_set.all():
            ret.append(reverse('episode', 
                               kwargs={'episode_id': episode.id, 
                                       'podcast_id': instance.id}))
        return ret

class EpisodeResource(ModelResource):
    """
    An episode associated with a podcast.
    """
    model = Episode
    fields = ('podcast', 'subtitle', 'title', 'author', 'updated', 'summary',
              'content', 'link', 'id',)
    ordering = ('-updated',)

    def podcast(self, instance):
        return reverse('podcast', kwargs={'id': instance.podcast.id})

