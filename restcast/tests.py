"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from restcast.models import WatchedRecord
import json

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


        

class PodcastResourceTest(TestCase):
    def test_get_list_request(self):
        resp = self.client.get('/resources/podcast/')
        self.assertEqual(resp.status_code, 200)

    def test_valid_post(self):
        resp = self.client.post('/resources/podcast/', {'link': 'http://shows.kingdomofloathing.com/ahd/videogameshotdog.xml'})
        self.assertEqual(resp.status_code, 201)

    def test_no_data_post(self):
        resp = self.client.post('/resources/podcast/', {})
        self.assertEqual(resp.status_code, 400)

    def test_get_non_existant_podcast(self):
        resp = self.client.get('/resources/podcast/1/')
        self.assertEqual(resp.status_code, 404)

    def test_get_existing_poscast(self):
        resp = self.client.post('/resources/podcast/', {'link': 'http://shows.kingdomofloathing.com/ahd/videogameshotdog.xml'})
        new_podcast_url = resp['Location']
        resp = self.client.get(new_podcast_url)
        self.assertEqual(resp.status_code, 200)

class EpisodeResourceTest(TestCase):
    def setUp(self):
        resp = self.client.post('/resources/podcast/', {'link': 'http://shows.kingdomofloathing.com/ahd/videogameshotdog.xml'})

    def test_get_episode_list(self):
        resp = self.client.get('/resources/podcast/1/episode/')
        self.assertEqual(resp.status_code, 200)

    def test_get_single_episode(self):
        resp = self.client.get('/resources/podcast/1/episode/1/')
        self.assertEqual(resp.status_code, 200)

    def test_get_non_existant_episode(self):
        resp = self.client.get('/resources/podcast/1/episode/500000/')
        self.assertEqual(resp.status_code, 404)

class WatchedRecordResourceTest(TestCase):
    fixtures = ['auth.json']

    def setUp(self):
        self.client.login(username='mreynolds', password='youcanttaketheskyfromme')
        resp = self.client.post('/resources/podcast/', {'link': 'http://shows.kingdomofloathing.com/ahd/videogameshotdog.xml'})

    def test_create_watched_record(self):
        resp = self.client.post('/resources/watched/', {'watched': True, 
                                                        'episode_id': 1})
        self.assertEqual(resp.status_code, 201)
        resp = self.client.get('/resources/watched/1/')
        self.assertEqual(resp.status_code, 200)

    def test_update_watched_record(self):
        resp = self.client.post('/resources/watched/', {'watched': True, 
                                                        'episode_id': 1})
        self.assertEqual(resp.status_code, 201)
        watched_record = WatchedRecord.objects.get(pk=1)
        self.assertEqual(watched_record.watched, True)
        resp = self.client.put('/resources/watched/1/', {'watched': False})
        self.assertEqual(resp.status_code, 200)
        watched_record = WatchedRecord.objects.get(pk=1)
        self.assertEqual(watched_record.watched, False)

    def test_watched_record_list(self):
        resp = self.client.post('/resources/watched/', {'watched': True, 
                                                        'episode_id': 1})
        self.assertEqual(resp.status_code, 201)
        resp = self.client.get('/resources/watched/')
        self.assertEqual(resp.status_code, 200)


class SubscriptionResourceTest(TestCase):
    fixtures = ['auth.json']

    def setUp(self):
        self.client.login(username='mreynolds', password='youcanttaketheskyfromme')
        resp = self.client.post('/resources/podcast/', {'link': 'http://shows.kingdomofloathing.com/ahd/videogameshotdog.xml'})

    def test_create_subscription(self):
        resp = self.client.post('/resources/subscription/', {'podcast_id': 1})
        self.assertEqual(resp.status_code, 201)
        resp = self.client.get('/resources/subscription/1/')
        self.assertEqual(resp.status_code, 200)

    def test_subscription_list(self):
        resp = self.client.get('/resources/subscription/', Accept='text/json')
        self.assertEqual(resp.status_code, 200)
        resp_json = json.loads(resp.content)
        self.assertEqual(0, len(resp_json))
        resp = self.client.post('/resources/subscription/', {'podcast_id': 1})
        self.assertEqual(resp.status_code, 201)
        resp = self.client.get('/resources/subscription/', Accept='text/json')
        self.assertEqual(resp.status_code, 200)
        resp_json = json.loads(resp.content)
        self.assertEqual(1, len(resp_json))
