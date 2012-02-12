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


        

class PodcastListViewTest(TestCase):
    def test_get_request(self):
        resp = self.client.get('/resources/podcast/')
        self.assertEqual(resp.status_code, 200)

    def test_valid_post(self):
        resp = self.client.post('/resources/podcast/', {'link': 'http://shows.kingdomofloathing.com/ahd/videogameshotdog.xml'})
        self.assertEqual(resp.status_code, 201)

    def test_no_data_post(self):
        resp = self.client.post('/resources/podcast/', {})
        self.assertEqual(resp.status_code, 400)
