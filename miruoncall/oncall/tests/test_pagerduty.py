# -*- coding: utf-8 -*-

import types
import unittest

import dateutil.parser
from mock import patch

from oncall.pagerduty import PagerDuty


class TestPagerDuty(unittest.TestCase):

    @patch('oncall.pagerduty.PagerDuty._query')
    def test_get_incidents(self, mock_query_resp):
        """
        Test getting a single pagination of incidents
        """
        mock_query_resp.return_value = {
            "incidents": [
                {
                    "id": "PT4KHLK",
                    "type": "incident",
                    "summary": "[#1234] The server is on fire.",
                    "incident_number": 1234,
                    "status": "resolved",
                    "title": "The server is on fire.",
                    "incident_key": "baf7cf21b1da41b4b0221008339ff357",
                    "urgency": "high"
                }
            ],
            "limit": 25,
            "offset": 0,
            "total": None,
            "more": False
        }

        pyduty = PagerDuty('abc123')

        incidents = pyduty.get_incidents(
            'ABCXYZ',
            since=dateutil.parser.parse('2019-01-01T06:42:09.668417+00:00'),
            until=dateutil.parser.parse('2019-01-01T06:52:09.668417+00:00')
        )

        self.assertTrue(isinstance(incidents, types.GeneratorType))

        next(incidents)

        mock_query_resp.assert_called_once_with(
            endpoint='incidents', method='GET',
            payload={
                'team_ids[]': 'ABCXYZ',
                'time_zone': 'UTC',
                'since': '2019-01-01T06:42:09.668417+00:00',
                'until': '2019-01-01T06:52:09.668417+00:00',
                'offset': 0
            }
        )

    @patch('oncall.pagerduty.PagerDuty._query')
    def test_get_incidents_pagination(self, mock_query_resp):
        """
        Test getting a paginated response of incidents
        """
        mock_query_resp.side_effect = [
            {
                "incidents": [
                    {
                        "id": "PT4KHLK",
                        "type": "incident",
                        "summary": "[#1234] The server is on fire.",
                        "incident_number": 1234,
                        "status": "resolved",
                        "title": "The server is on fire.",
                        "incident_key": "baf7cf21b1da41b4b0221008339ff357",
                        "urgency": "high"
                    }
                ],
                "limit": 25,
                "offset": 0,
                "total": None,
                "more": True
            },
            {
                "incidents": [
                    {
                        "id": "PT4KHLK",
                        "type": "incident",
                        "summary": "[#1234] The server is on fire.",
                        "incident_number": 1234,
                        "status": "resolved",
                        "title": "The server is on fire.",
                        "incident_key": "baf7cf21b1da41b4b0221008339ff357",
                        "urgency": "high"
                    }
                ],
                "limit": 25,
                "offset": 0,
                "total": None,
                "more": False
            }
        ]

        pyduty = PagerDuty('abc123')

        incidents = pyduty.get_incidents(
            'ABCXYZ',
            since=dateutil.parser.parse('2019-01-01T06:42:09.668417+00:00'),
            until=dateutil.parser.parse('2019-01-01T06:52:09.668417+00:00')
        )

        self.assertTrue(isinstance(incidents, types.GeneratorType))

        # Skip the two pagination pages
        next(incidents)
        next(incidents)

        self.assertRaises(StopIteration, next, incidents)

    @patch('oncall.pagerduty.PagerDuty._query')
    def test_get_incident(self, mock_query_resp):
        """
        Test getting a single incident
        """
        mock_query_resp.return_value = {
            "incident": {
                "id": "PT4KHLK",
                "type": "incident",
                "summary": "[#1234] The server is on fire.",
                "incident_number": 1234,
                "status": "resolved",
                "title": "The server is on fire.",
            },
            "urgency": "high"
        }

        pyduty = PagerDuty('abc123')
        pyduty.get_incident('ABCXYZ')

        mock_query_resp.assert_called_once_with(
            endpoint='incidents/ABCXYZ', method='GET'
        )

    @patch('oncall.pagerduty.PagerDuty._query')
    def test_get_teams(self, mock_query_resp):
        """
        Test getting a single pagination of teams
        """
        mock_query_resp.return_value = {
            "teams": [
                {
                    "id": "PQ9K7I8",
                    "type": "team",
                    "summary": "Engineering",
                    "self": "https://api.pagerduty.com/teams/PQ9K7I8",
                    "html_url": "https://subdomain.pagerduty.com/teams/PQ9K7I8",
                    "name": "Engineering",
                    "description": "All engineering"
                }
            ],
            "limit": 25,
            "offset": 0,
            "total": None,
            "more": False
        }

        pyduty = PagerDuty('abc123')
        team = pyduty.get_teams()

        self.assertTrue(isinstance(team, types.GeneratorType))
        next(team)

        mock_query_resp.assert_called_once_with(
            endpoint='teams', method='GET', payload={'offset': 0}
        )

    @patch('oncall.pagerduty.PagerDuty._query')
    def test_get_teams_pagination(self, mock_query_resp):
        """
        Test getting a paginated response of teams
        """
        mock_query_resp.side_effect = [
            {
                "teams": [
                    {
                        "id": "PQ9K7I8",
                        "type": "team",
                        "summary": "Engineering",
                        "self": "https://api.pagerduty.com/teams/PQ9K7I8",
                        "html_url": "https://subdomain.pagerduty.com/teams/PQ9K7I8",
                        "name": "Engineering",
                        "description": "All engineering"
                    }
                ],
                "limit": 25,
                "offset": 0,
                "total": None,
                "more": True
            },
            {
                "teams": [
                    {
                        "id": "PQ9K7I8",
                        "type": "team",
                        "summary": "Engineering",
                        "self": "https://api.pagerduty.com/teams/PQ9K7I8",
                        "html_url": "https://subdomain.pagerduty.com/teams/PQ9K7I8",
                        "name": "Engineering",
                        "description": "All engineering"
                    }
                ],
                "limit": 25,
                "offset": 0,
                "total": None,
                "more": False
            },
        ]

        pyduty = PagerDuty('abc123')
        team = pyduty.get_teams()

        self.assertTrue(isinstance(team, types.GeneratorType))

        # Skip the two pagination pages
        next(team)
        next(team)

        self.assertRaises(StopIteration, next, team)

    @patch('oncall.pagerduty.PagerDuty._query')
    def test_get_schedules(self, mock_query_resp):
        """
        Test getting a specific teams list of schedules
        """
        mock_query_resp.return_value = {
            "schedules": [
                {
                    "id": "PI7DH85",
                    "type": "schedule",
                    "summary": "Daily Engineering Rotation",
                    "self": "https://api.pagerduty.com/schedules/PI7DH85",
                    "html_url": "https://subdomain.pagerduty.com/schedules/PI7DH85",
                    "name": "Daily Engineering Rotation",
                    "time_zone": "America/New_York",
                    "description": "Rotation schedule for engineering",
                }
            ],
            "limit": 100,
            "offset": 0,
            "total": None,
            "more": False
        }

        pyduty = PagerDuty('abc123')
        schedules = pyduty.get_schedules('TEAMID')

        self.assertTrue(isinstance(schedules, types.GeneratorType))

        # Skip the two pagination pages
        next(schedules)

        self.assertRaises(StopIteration, next, schedules)

        mock_query_resp.assert_called_once_with(
            endpoint='schedules', method='GET', payload={'offset': 25, 'team_ids[]': 'TEAMID'}
        )

    @patch('oncall.pagerduty.PagerDuty._query')
    def test_get_schedule(self, mock_query_resp):
        """
        Test getting a specific schedule
        """
        mock_query_resp.return_value = {}

        pyduty = PagerDuty('abc123')

        pyduty.get_schedule(
            'ABC123',
            dateutil.parser.parse('2019-01-01T06:42:09.668417+00:00'),
            dateutil.parser.parse('2019-01-01T06:52:09.668417+00:00')
        )

        mock_query_resp.assert_called_once_with(
            endpoint='schedules/ABC123',
            method='GET',
            payload={
                'id': 'ABC123',
                'time_zone': 'UTC',
                'since': '2019-01-01T06:42:09.668417+00:00',
                'until': '2019-01-01T06:52:09.668417+00:00'
            }
        )

    @unittest.skip('Need to implement')
    def test_query(self):
        """
        Test making HTTPS queries to PagerDuty
        """
        pass

    @unittest.skip('Need to implement')
    def test_query_failure(self):
        """
        Test failing to query PagerDuty
        """
        pass
