# Create your views here.
import feedparser
from django.http import HttpResponse
from restcast.models import Podcast
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
            link = podcast.feed.link,
            title = podcast.feed.title,
            rights = podcast.feed.rights,
            author = podcast.feed.author, 
            email = podcast.feed.authors[0]['email'],
            summary = podcast.feed.summary
            )

        podcast_model.save()
    
    return HttpResponse()

