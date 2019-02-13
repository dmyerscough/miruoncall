# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from mock import patch
from rest_framework.test import APIClient

from oncall.models import Incidents, Team


class TestOncallView(TestCase):

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

        self.incident = Incidents.objects.get_or_create(
            id='96e3d488-52b8-4b86-906e-8bc5b3b7504b',
            title='Down Master DB',
            description='Down Master DB',
            summary='Down Master DB',
            status='triggered',
            created_at=self.creation_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            incident_id='PIJK3SJ',
            urgency='high',
            team=self.team,
        )

    def test_listing_incidents(self):
        """
        Test listing all incidents for a team
        """
        resp = self.client.get(
            reverse('incidents', kwargs={'team_id': '7de98e0c-8bf9-414c-b397-05acb136935e'})
        )

        self.assertEqual(resp.json(), {
            'incident_count': {self.creation_time.strftime('%Y-%m-%d'): 1},
            'incidents': [
                    {
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
                    }
                ]
            }
        )

    def test_listing_for_none_existent_team(self):
        """
        Test listing incidents for a team that does not exist
        """
        resp = self.client.get(
            reverse('incidents', kwargs={'team_id': '9de98e0c-8bf9-414c-b397-05acb136935f'})
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {'error': f'9de98e0c-8bf9-414c-b397-05acb136935f does not exist'})

    def test_listing_incidents_invalid_date_rage(self):
        """
        Test getting incidents with since being greater than until
        """
        resp = self.client.get(
            reverse('incidents', kwargs={'team_id': '7de98e0c-8bf9-414c-b397-05acb136935e'}), {'since': '05-01-2019', 'until': '01-01-2019'}
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {'error': 'since cannot be newer than until'})

    def test_incident_annotation(self):
        """
        Test creating an annotation for an incident
        """
        with patch.object(timezone, 'now', return_value=self.creation_time.strftime('%Y-%m-%dT%H:%M:%SZ')):
            resp = self.client.post(
                reverse('incidents', kwargs={'team_id': '7de98e0c-8bf9-414c-b397-05acb136935e'}),
                {'incident_ids': '96e3d488-52b8-4b86-906e-8bc5b3b7504b', 'annotation': 'Rebooted server', 'actionable': False}
            )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {'message': 'successfully updated'})

        resp = self.client.get(
            reverse('incidents', kwargs={'team_id': '7de98e0c-8bf9-414c-b397-05acb136935e'})
        )
        self.maxDiff = None
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {
            'incident_count': {self.creation_time.strftime('%Y-%m-%d'): 1},
            'incidents': [
                    {
                        'actionable': False,
                        'annotation': {
                            'annotation': 'Rebooted server',
                            'created_at': self.creation_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                            'created_by': 'DamianMyerscough'
                        },
                        'created_at': self.creation_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        'description': 'Down Master DB',
                        'id': '96e3d488-52b8-4b86-906e-8bc5b3b7504b',
                        'incident_id': 'PIJK3SJ',
                        'status': 'triggered',
                        'summary': 'Down Master DB',
                        'title': 'Down Master DB',
                        'urgency': 'high'
                    }
                ]
            }
        )

    def test_updating_multiple_incidents(self):
        """
        Test updating multiple incidents
        """
        with patch.object(timezone, 'now', return_value=self.creation_time.strftime('%Y-%m-%dT%H:%M:%SZ')):
            Incidents.objects.create(
                id='96e3d488-52b8-4b86-906e-8bc5b3b7504c',
                title='Down Replica DB',
                description='Down Replica DB',
                summary='Down Replica DB',
                status='triggered',
                created_at=self.creation_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                incident_id='PIJK3SK',
                urgency='high',
                team=self.team,
            )

            resp = self.client.post(
                reverse('incidents', kwargs={'team_id': '7de98e0c-8bf9-414c-b397-05acb136935e'}),
                {
                    'incident_ids': '96e3d488-52b8-4b86-906e-8bc5b3b7504b,96e3d488-52b8-4b86-906e-8bc5b3b7504c',
                    'annotation': 'Rebooted server'
                }
            )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {'message': 'successfully updated'})

        resp = self.client.get(
            reverse('incidents', kwargs={'team_id': '7de98e0c-8bf9-414c-b397-05acb136935e'})
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {
            'incident_count': {self.creation_time.strftime('%Y-%m-%d'): 2},
            'incidents': [
                {
                    'actionable': True,
                    'annotation': {
                        'annotation': 'Rebooted server',
                        'created_at': self.creation_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        'created_by': 'DamianMyerscough'
                    },
                    'created_at': self.creation_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'description': 'Down Master DB',
                    'id': '96e3d488-52b8-4b86-906e-8bc5b3b7504b',
                    'incident_id': 'PIJK3SJ',
                    'status': 'triggered',
                    'summary': 'Down Master DB',
                    'title': 'Down Master DB',
                    'urgency': 'high'
                },
                {
                    'actionable': True,
                    'annotation': {
                        'annotation': 'Rebooted server',
                        'created_at': self.creation_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        'created_by': 'DamianMyerscough'
                    },
                    'created_at': self.creation_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'description': 'Down Replica DB',
                    'id': '96e3d488-52b8-4b86-906e-8bc5b3b7504c',
                    'incident_id': 'PIJK3SK',
                    'status': 'triggered',
                    'summary': 'Down Replica DB',
                    'title': 'Down Replica DB',
                    'urgency': 'high'
                }
            ]
        })

    def test_incident_invalid_incident_id(self):
        """
        Test updating an invalid incident id
        """
        resp = self.client.post(
            reverse('incidents', kwargs={'team_id': '7de98e0c-8bf9-414c-b397-05acb136935e'}),
            {'incident_ids': '96e3d488', 'annotation': 'Rebooted server'}
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {'error': 'Invalid incident id: 96e3d488'})

    def test_incident_missing_incident_id(self):
        """
        Test updating an incident with a missing incidents_ids
        """
        resp = self.client.post(
            reverse('incidents', kwargs={'team_id': '7de98e0c-8bf9-414c-b397-05acb136935e'}),
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {'error': 'incident_ids is a required argument'})

    def test_incident_updating_none_existent_incident(self):
        """
        Test updating an incident that does not exist
        """
        resp = self.client.post(
            reverse('incidents', kwargs={'team_id': '7de98e0c-8bf9-414c-b397-05acb136935e'}),
            {'incident_ids': '76e3d488-52b8-4b86-906e-8bc5b3b7504e', 'annotation': 'Rebooted server'}
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {'error': 'Incident 76e3d488-52b8-4b86-906e-8bc5b3b7504e does not exist'})

    def test_incident_update_none_existent_team(self):
        """
        Test updating an incident for a team that does not exist
        """
        resp = self.client.post(
            reverse('incidents', kwargs={'team_id': '8de98e0c-8bf9-414c-b397-05acb136956e'}),
            {'incident_ids': '76e3d488-52b8-4b86-906e-8bc5b3b7504e', 'actionable': True}
        )

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {'error': '8de98e0c-8bf9-414c-b397-05acb136956e does not exist'})
