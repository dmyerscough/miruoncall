# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from mock import patch
from rest_framework.test import APIClient

from oncall.models import Annotations, Incidents, Team


class TestIncidentView(TestCase):

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

        self.team, _ = Team.objects.get_or_create(
            id='7de98e0c-8bf9-414c-b397-05acb136935e',
            name='PANW SRE',
            team_id='PANW',
            summary='The Oncall Team for XYZ',
        )

        self.creation_time = timezone.now()

        with patch('django.utils.timezone.now') as mock_timezone:
            mock_timezone.return_value = self.creation_time

            self.annotation = Annotations.objects.create(
                annotation='Testing Annotation',
                created_by=self.user,
                created_at=self.creation_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            )

            self.incident = Incidents.objects.get_or_create(
                id='96e3d488-52b8-4b86-906e-8bc5b3b7504b',
                title='Down Master DB',
                description='Down Master DB',
                summary='Down Master DB',
                status='triggered',
                incident_id='PIJK3SJ',
                urgency='high',
                team=self.team,
                created_at=self.creation_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                annotation=self.annotation,
            )

    def test_retrieving_incident(self):
        """
        Test retrieving an incident
        """
        resp = self.client.get(
            reverse('incident', kwargs={
                'team_id': '7de98e0c-8bf9-414c-b397-05acb136935e', 'incident_id': '96e3d488-52b8-4b86-906e-8bc5b3b7504b'
            }),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {
            'actionable': True,
            'annotation': {
                'annotation': 'Testing Annotation',
                'created_at': self.creation_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'created_by': self.user.username
            },
            'created_at': self.creation_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'description': 'Down Master DB',
            'id': '96e3d488-52b8-4b86-906e-8bc5b3b7504b',
            'incident_id': 'PIJK3SJ',
            'status': 'triggered',
            'summary': 'Down Master DB',
            'title': 'Down Master DB',
            'urgency': 'high'
        })

    def test_deleting_annotation(self):
        """
        Test deleting an annotation from an incident
        """
        resp = self.client.delete(
            reverse('incident', kwargs={
                'team_id': '7de98e0c-8bf9-414c-b397-05acb136935e', 'incident_id': '96e3d488-52b8-4b86-906e-8bc5b3b7504b'
            }),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {'message': 'annotation removed'})

        resp = self.client.get(
            reverse('incident', kwargs={
                'team_id': '7de98e0c-8bf9-414c-b397-05acb136935e', 'incident_id': '96e3d488-52b8-4b86-906e-8bc5b3b7504b'
            }),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {
            'actionable': True,
            'annotation': None,
            'created_at': self.creation_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'description': 'Down Master DB',
            'id': '96e3d488-52b8-4b86-906e-8bc5b3b7504b',
            'incident_id': 'PIJK3SJ',
            'status': 'triggered',
            'summary': 'Down Master DB',
            'title': 'Down Master DB',
            'urgency': 'high'
        })
