# Create your views here.
from djangorestframework.compat import View
from djangorestframework.views import ModelView
from djangorestframework.mixins import ResponseMixin, ReadModelMixin, ListModelMixin
from djangorestframework.renderers import DEFAULT_RENDERERS
from djangorestframework.response import Response
from djangorestframework import status
from djangorestframework.permissions import IsAuthenticated

import feedparser
from time import mktime
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from restcast.models import Podcast, Episode, WatchedRecord
from restcast.resources import WatchedRecordResource, PodcastResource
from restcast.forms import WatchedRecordCreateForm, PodcastCreateForm

class PodcastListView(ListModelMixin, ModelView):
    resource = PodcastResource
    form = PodcastCreateForm
    def post(self, request):
        link = self.CONTENT['link']
        podcast = feedparser.parse(link)

        podcast_model = Podcast(
            last_updated = datetime.fromtimestamp(mktime(podcast.updated_parsed)),
            version = podcast.version,
            itunes_namespace = podcast.namespaces['itunes'],
            publisher = podcast.feed.publisher,
            subtitle = podcast.feed.subtitle,
            link = link,
            title = podcast.feed.title,
            rights = podcast.feed.rights,
            author = podcast.feed.author, 
            email = podcast.feed.authors[0]['email'],
            summary = podcast.feed.summary
            )

        podcast_model.save()
        podcast_model.load_episodes()
        headers = {}
        if hasattr(podcast_model, 'get_absolute_url'):
            headers['Location'] = podcast_model.get_absolute_url()
        return Response(status.HTTP_201_CREATED, podcast_model, headers)
        
    

class ReadModelView(ReadModelMixin, ModelView):
    """
    A view which provides default operations for read/update/delete against a model instance.
    """
    _suffix = 'Read'


class WatchedRecordInstanceView(ReadModelMixin, ModelView):
    resource = WatchedRecordResource
    permissions = [IsAuthenticated]

    def get(self, request, pk):
        model = self.resource.model
        self.model_instance = get_object_or_404(model, pk=pk, user=request.user.id)
        return self.model_instance

    def put(self, request, pk):
        model = self.resource.model
        # TODO: update on the url of a non-existing resource url doesn't work correctly at the moment - will end up with a new url
        self.model_instance = get_object_or_404(model, pk=pk, user=request.user.id)
        self.model_instance.watched = self.CONTENT['watched']
        self.model_instance.save()
        return self.model_instance


class WatchedRecordListView(ModelView):
    resource = WatchedRecordResource
    permissions = [IsAuthenticated]
    form = WatchedRecordCreateForm
    def get(self, request, *args, **kwargs):
        queryset = WatchedRecord.objects.filter(user = request.user)

        if hasattr(self, 'resource'):
            ordering = getattr(self.resource, 'ordering', None)
        else:
            ordering = None

        if ordering:
            queryset = queryset.order_by(*args)
        return queryset.filter(**kwargs)
    
    def post(self, request):
        # Copy the dict to keep self.CONTENT intact
        content = dict(self.CONTENT)
        print 'content ', content
        try:
            instance = WatchedRecord.objects.get(user=request.user, 
                                      episode = content['episode_id'])
            instance.watched = content['watched']
        except ObjectDoesNotExist:
            instance = WatchedRecord(user=request.user, 
                                     watched = content['watched'],
                                     episode_id = content['episode_id'])
        instance.save()

        headers = {}
        if hasattr(instance, 'get_absolute_url'):
            headers['Location'] = self.resource(self).url(instance)
        return Response(status.HTTP_201_CREATED, instance, headers)
