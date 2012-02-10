# Create your views here.
from djangorestframework.compat import View
from djangorestframework.mixins import ResponseMixin
from djangorestframework.renderers import DEFAULT_RENDERERS
from djangorestframework.response import Response

import feedparser
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from restcast.models import Podcast, Episode
from time import mktime
from datetime import datetime

def import_podcast(request):
    podcastXml = request.GET.get('podcastXml')
    if podcastXml:
        podcast = feedparser.parse(podcastXml)

        podcast_model = Podcast(
            last_updated = datetime.fromtimestamp(mktime(podcast.updated_parsed)),
            version = podcast.version,
            itunes_namespace = podcast.namespaces['itunes'],
            publisher = podcast.feed.publisher,
            subtitle = podcast.feed.subtitle,
            podcast_xml = podcastXml,
            title = podcast.feed.title,
            rights = podcast.feed.rights,
            author = podcast.feed.author, 
            email = podcast.feed.authors[0]['email'],
            summary = podcast.feed.summary
            )

        podcast_model.save()
        podcast_model.load_episodes()
    
    return HttpResponse()



class EpisodeInstanceView(ResponseMixin, View):
    """View for a single instance of an episode"""
    renderers = DEFAULT_RENDERERS

    def get(self, request, podcast_id, episode_id):
        
        episode = get_object_or_404(Episode, podcast__id=podcast_id, pk = episode_id)

        episode_dict = episode.to_dict(request.user)

        response = Response(200, episode_dict)
        return self.render(response)
