from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
import feedparser
from time import mktime
from datetime import datetime


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
    
    def load_episodes(self):
        feed = feedparser.parse(self.link)
        for entry in feed.entries:
            count = Episode.objects.filter(link=entry.links[0]['href']).count()
            print 'count: ', count
            if (count == 0):
                episode = Episode(
                    podcast=self,
                    subtitle=entry.subtitle,
                    title=entry.title,
                    author=entry.author,
                    updated=datetime.fromtimestamp(mktime(entry.updated_parsed)),
                    summary=entry.summary,
                    link=entry.links[0]['href']
                    )
                episode.save()

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

    def __unicode__(self):
        return '%s has %s %s' % (self.user, 'watched' if self.watched else 'not watched', self.episode)

    def get_absolute_url(self):
        return reverse('watched-record', kwargs={'pk': self.id})
    

