# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from oncall.models import Team


class TestTeams(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            username="DamianMyerscough",
        )
        self.user.set_password('abc123')
        self.user.save()

        self.client.login(
            username="DamianMyerscough",
            password="abc123",
        )

    def test_listing_teams(self):
        """
        Test listing teams
        """
        Team.objects.create(
            id='7de98e0c-8bf9-414c-b397-05acb136935e',
            name='Example',
            team_id='ABC123',
        )

        resp = self.client.get(
            reverse('teams')
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {'teams': [{'id': '7de98e0c-8bf9-414c-b397-05acb136935e', 'name': 'Example'}]})
