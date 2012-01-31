from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Podcast(models.Model):
    last_updated = models.DateField(blank=True)
    version = models.CharField(max_length=128,blank=True)
    itunes_namespace = models.CharField(max_length=256,blank=True)
    publisher = models.CharField(max_length=256,blank=True)
    subtitle = models.CharField(max_length=256,blank=True)
    link = models.URLField(blank=True)
    title = models.CharField(max_length=256,blank=True)
    # image = models.ImageField(upload_to='podcastIcons')
    rights = models.CharField(max_length=256,blank=True)
    author = models.CharField(max_length=256,blank=True)
    # authors email
    email = models.EmailField(blank=True)
    summary = models.TextField(blank=True)
    

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


class WatchedRecord(models.Model):
    user = models.ForeignKey(User)
    episode = models.ForeignKey(Episode)
    watched = models.BooleanField()


