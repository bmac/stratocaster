from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User

class Podcast(models.Model):
    last_updated = models.DateField(blank=True)
    version = models.CharField(max_length=128,blank=True)
    itunes_namespace = models.CharField(max_length=256,blank=True)
    publisher = models.CharField(max_length=256,blank=True)
    subtitle = models.CharField(max_length=256,blank=True)
    link = models.URLField(blank=True)
#    podcast_xml = models.URLField(blank=True)
    title = models.CharField(max_length=256,blank=True)
    # image = models.ImageField(upload_to='podcastIcons')
    rights = models.CharField(max_length=256,blank=True)
    author = models.CharField(max_length=256,blank=True)
    # authors email
    email = models.EmailField(blank=True)
    summary = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('podcast', kwargs={'id': self.id})

class Episode(models.Model):
    podcast = models.ForeignKey(Podcast)
    subtitle = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    # itunes_explicit = 
    author = models.CharField(max_length=256)
    updated = models.DateField()
    summary = models.TextField()
    content = models.TextField()
    link = models.URLField()
    episode_id = models.CharField(max_length=256)

    def __unicode__(self):
        return '%s: %s' % (self.podcast.title, self.title)

    def get_absolute_url(self):
        return reverse('episode', kwargs={'id': self.id, 
                                          'podcast': self.podcast.id})

class WatchedRecord(models.Model):
    user = models.ForeignKey(User)
    episode = models.ForeignKey(Episode)
    watched = models.BooleanField()

    @staticmethod 
    def get_or_create(**kwargs):
        records = list(WatchedRecord.objects.filter(**kwargs))
        if records:
            return records[0]
        watched_record = WatchedRecord(**kwargs)
        watched_record.save()
        return watched_record
        

    def __unicode__(self):
        return '%s has %s %s' % (self.user, 'watched' if self.watched else 'not watched', self.episode)

    def get_absolute_url(self):
        return reverse('watched-record', kwargs={'pk': self.id})
    
class Subscription(models.Model):
    user = models.ForeignKey(User)
    podcast = models.ForeignKey(Podcast)

    def __unicode__(self):
        return '%s has subscribed to %s' % (self.user, self.podcast)

    def get_absolute_url(self):
        return reverse('subscription', kwargs={'pk': self.id})
