"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


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
