# -*- coding: utf-8 -*-

import uuid
from unittest import skip

from django.test import TestCase
from django.utils import timezone
from mock import MagicMock, patch

from oncall.models import Incidents, Team
from oncall.tasks import (_populate_alerts, _update_incident, populate_alerts,
                          populate_teams, update_incidents)


class TestCeleryTasks(TestCase):

    @patch('oncall.tasks._populate_alerts')
    def test_populate_alerts(self, mock_populate_alerts):
        """
        Test checking teams to populate alerts
        """
        current_time = timezone.now()

        with patch.object(timezone, 'now', return_value=current_time):
            Team.objects.create(
                id='b322c6ab-3170-4ff2-b4d8-34d0a4371c9d',
                name='PANW',
                team_id='PANW123',
                summary='PANW SRE'
            )

            self.assertTrue(populate_alerts())

        mock_populate_alerts.delay.assert_called_once_with(
            since=current_time,
            team_id=uuid.UUID('b322c6ab-3170-4ff2-b4d8-34d0a4371c9d'),
            until=current_time,
        )

    @patch('oncall.tasks.PagerDuty')
    def test_populate_alerts_private(self, mock_pagerduty):
        """
        Test populating alerts
        """
        mock_incidents = MagicMock()
        mock_incidents.get_incidents.return_value = [
            [
                {
                    'id': 'PT4KHLK',
                    'summary': '[#1234] The server is on fire.',
                    'incident_number': 1234,
                    'created_at': '2015-10-06T21:30:42Z',
                    'status': 'resolved',
                    'title': 'The server is on fire.',
                    'incident_key': 'baf7cf21b1da41b4b0221008339ff357',
                    'last_status_change_at': '2015-10-06T21:38:23Z',
                    'urgency': 'high'
                }
            ]
        ]

        mock_pagerduty.return_value = mock_incidents

        current_time = timezone.now()

        with patch.object(timezone, 'now', return_value=current_time):
            Team.objects.create(
                id='b322c6ab-3170-4ff2-b4d8-34d0a4371c9d',
                name='PANW',
                team_id='PANW123',
                summary='PANW SRE'
            )

        self.assertTrue(
            _populate_alerts(team_id='b322c6ab-3170-4ff2-b4d8-34d0a4371c9d', since=current_time.isoformat(), until=current_time.isoformat())
        )

        incident = Incidents.objects.get(incident_id='PT4KHLK')

        self.assertEqual(incident.incident_id, 'PT4KHLK')
        self.assertEqual(incident.title, 'The server is on fire.')
        self.assertEqual(incident.summary, '[#1234] The server is on fire.')
        self.assertEqual(incident.description, 'No description')

    @skip('Needs implemented')
    def test_populate_alerts_request_failure(self):
        pass

    @patch('oncall.tasks.PagerDuty')
    def test_populate_teams(self, mock_teams):
        """
        Test populating teams
        """
        mock_team = MagicMock()
        mock_team.get_teams.return_value = [
            [
                {
                    "id": "PQ9K7I8",
                    "type": "team",
                    "summary": "Engineering",
                    "self": "https://api.pagerduty.com/teams/PQ9K7I8",
                    "html_url": "https://subdomain.pagerduty.com/teams/PQ9K7I8",
                    "name": "Engineering",
                    "description": "All engineering"
                }
            ]
        ]

        mock_teams.return_value = mock_team

        self.assertTrue(populate_teams())

    @skip('Needs implemented')
    def test_populate_teams_request_failure(self):
        pass

    @patch('oncall.tasks.PagerDuty')
    def test_update_incident_helper_status_mismatch(self, mock_incident):
        """
        Test incident helper when the status does not match the status stored in the database
        """
        mock_incident_ = MagicMock()
        mock_incident_.get_incident.return_value = {
            'id': 'PT4KHLK',
            'type': 'incident',
            'summary': '[#1234] The server is on fire.',
            'self': 'https://api.pagerduty.com/incidents/PT4KHLK',
            'html_url': 'https://subdomain.pagerduty.com/incidents/PT4KHLK',
            'incident_number': 1234,
            'created_at': '2015-10-06T21:30:42Z',
            'status': 'resolved',
            'title': 'The server is on fire.',
            'urgency': 'high'
        }

        mock_incident.return_value = mock_incident_

        Incidents.objects.create(
            id='96e3d488-52b8-4b86-906e-8bc5b3b7504b',
            title='Down Replica DB',
            description='Down Replica DB',
            summary='Down Replica DB',
            status='triggered',
            created_at=timezone.now(),
            incident_id='PT4KHLK',
            urgency='high',
            team=Team.objects.create(
                name='PANW SRE',
                team_id='PANW',
                summary='The Oncall Team for XYZ',
            )
        )

        self.assertTrue(_update_incident('96e3d488-52b8-4b86-906e-8bc5b3b7504b'))
        self.assertEqual(Incidents.objects.get(id='96e3d488-52b8-4b86-906e-8bc5b3b7504b').status, 'resolved')

        mock_incident_.get_incident.assert_called_once_with(incident_id='PT4KHLK')

    @patch('oncall.tasks._update_incident')
    def test_update_incident(self, mock_update_incident):
        """
        Test updaing an incident that is not marked as resolved
        """
        current_time = timezone.now()

        with patch.object(timezone, 'now', return_value=current_time):
            Incidents.objects.create(
                id='96e3d488-52b8-4b86-906e-8bc5b3b7504b',
                title='Down Replica DB',
                description='Down Replica DB',
                summary='Down Replica DB',
                status='triggered',
                created_at=timezone.now(),
                incident_id='PT4KHLK',
                urgency='high',
                team=Team.objects.create(
                    name='PANW SRE',
                    team_id='PANW',
                    summary='The Oncall Team for XYZ',
                )
            )

            self.assertTrue(update_incidents())

        mock_update_incident.delay.assert_called_once_with(
            incident_id=uuid.UUID('96e3d488-52b8-4b86-906e-8bc5b3b7504b'),
        )
