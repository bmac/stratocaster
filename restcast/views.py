# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from restcast.models import Episode, WatchedRecord

def update_watched_record(request, podcast_id, episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    watched_record = WatchedRecord.get_or_create(episode=episode, user=request.user)
    if request.method == 'POST':
        watched_record.watched = request.POST.get('listened', False)
        watched_record.save()
    return HttpResponse(watched_record.watched)
