from djangorestframework.views import ModelView
from djangorestframework.mixins import ReadModelMixin, ListModelMixin, ModelMixin
from djangorestframework.response import Response, ErrorResponse
from djangorestframework import status
from djangorestframework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist

from restcast.models import WatchedRecord, Subscription
from restcast.resources import WatchedRecordResource, PodcastResource, SubscriptionResource
from restcast.forms import WatchedRecordCreateForm, PodcastCreateForm, SubscriptionForm

import podcastloader

class PodcastListView(ListModelMixin, ModelView):
    resource = PodcastResource
    form = PodcastCreateForm
    def post(self, request):
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


class ReadUserModelMixin(ModelMixin):
    permissions = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        model = self.resource.model
        # many-to-many objects use the lower-cased object_name + "_set",
        # but this can be overridden with the "related_name" option.        
        # because we can not exted the user object I think 
        # object_name.lower() + '_set' should be ok here
        try: 
            relationship_name = model._meta.object_name.lower() + '_set'
            queryset = getattr(request.user, relationship_name)
            self.model_instance = queryset.get(**kwargs)
        except model.DoesNotExist:
            raise ErrorResponse(status.HTTP_404_NOT_FOUND, None, {})
        return self.model_instance

class UpdateUserModelMixin(ModelMixin):
    permissions = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        model = self.resource.model
        try: 
            relationship_name = model._meta.object_name.lower() + '_set'
            queryset = getattr(request.user, relationship_name)
            self.model_instance = queryset.get(**kwargs)
            for (key, val) in self.CONTENT.items():
                setattr(self.model_instance, key, val)
        except model.DoesNotExist:
            raise ErrorResponse(status.HTTP_404_NOT_FOUND, None, {})
        self.model_instance.save()
        return self.model_instance

class ReadUpdateUserModelView(ReadUserModelMixin, UpdateUserModelMixin, ModelView):
    """
    A view which provides default operations for read/write against a model instance
    addociated with a specific user.
    """
    _suffix = 'ReadUpdateUser'


class ListUserModelMixin(ModelMixin):
    """
    Behavior to list a set of `model` instances on GET requests
    """

    def get(self, request, *args, **kwargs):
        model = self.resource.model
        ordering = self.get_ordering()
        relationship_name = model._meta.object_name.lower() + '_set'
        queryset = getattr(request.user, relationship_name)
        queryset = queryset.filter(self.build_query(**kwargs))
        if ordering:
            queryset = queryset.order_by(*ordering)

        return queryset


class WatchedRecordListView(ListUserModelMixin, ModelView):
    resource = WatchedRecordResource
    permissions = [IsAuthenticated]
    form = WatchedRecordCreateForm
    
    def post(self, request):
        # Copy the dict to keep self.CONTENT intact
        content = dict(self.CONTENT)
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
            headers['Location'] = instance.get_absolute_url()
        return Response(status.HTTP_201_CREATED, instance, headers)

# todo refactor this with watchedRecordListView to use less code
class SubscriptionListView(ListUserModelMixin, ModelView):
    resource = SubscriptionResource
    permissions = [IsAuthenticated]
    form = SubscriptionForm
    
    def post(self, request):
        # Copy the dict to keep self.CONTENT intact
        content = dict(self.CONTENT)
        try:
            instance = Subscription.objects.get(user=request.user, 
                                      podcast = content['podcast_id'])
        except ObjectDoesNotExist:
            instance = Subscription(user=request.user, 
                                     podcast_id = content['podcast_id'])
        instance.save()

        headers = {}
        if hasattr(instance, 'get_absolute_url'):
            headers['Location'] = instance.get_absolute_url()
        return Response(status.HTTP_201_CREATED, instance, headers)
