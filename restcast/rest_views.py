from djangorestframework.views import ModelView
from djangorestframework.mixins import ReadModelMixin, ListModelMixin
from djangorestframework.response import Response
from djangorestframework import status

from restcast.resources import PodcastResource
from restcast.forms import PodcastCreateForm

import podcastloader

class PodcastListView(ListModelMixin, ModelView):
    resource = PodcastResource
    form = PodcastCreateForm
    def put(self, request):
        link = self.CONTENT['link']
        podcast = podcastloader.create_podcast_form_feed_link(link)
        podcastloader.load_episodes_for_podcast(podcast)
        
        headers = {}
        if hasattr(podcast, 'get_absolute_url'):
            headers['Location'] = podcast.get_absolute_url()
        return Response(status.HTTP_201_CREATED, podcast, headers)
        
    

class ReadModelView(ReadModelMixin, ModelView):
    """
    A view which provides default operations for read against a model instance.
    """
    _suffix = 'Read'
