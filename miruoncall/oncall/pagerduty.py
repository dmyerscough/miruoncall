# -*- coding: utf-8 -*-

from urllib.parse import urljoin

from django.utils import timezone
from requests import Request, Session


class RequestFailure(Exception):
    pass


class InvalidTimeRange(Exception):
    pass


class PagerDuty(object):

    PAGERDUTY_ENDPOINT = "https://api.pagerduty.com"

    def __init__(self, api):

        self.api = api

    def _query(self, method, endpoint, payload=None, timeout=5):
        """
        Make HTTPS request to PagerDuty

        :param method: HTTP method
        :param endpoint: HTTP endpoint to
        :return: Generator Json Response
        """
        if payload is None:
            payload = {}

        headers = {
            'Accept': 'application/vnd.pagerduty+json;version=2',
            'Authorization': f'Token token={self.api}',
        }

        session = Session()

        request = Request(
            method=method,
            url=urljoin(self.PAGERDUTY_ENDPOINT, endpoint),
            params=payload,
            headers=headers
        )

        prep = session.prepare_request(request)
        resp = session.send(prep, timeout=timeout)

        if resp.status_code != 200:
            raise RequestFailure(f"Requesting: {endpoint} returned a status code: {resp.status_code}")

        return resp.json()

    @staticmethod
    def _check_date(since, until):
        """
        Basic datetime validation

        :param since: PagerDutys since field
        :param until: PagerDutys until field

        :return: None
        """
        if since > until:
            raise InvalidTimeRange("Since time cannot be newer than until time")

        if since > timezone.now() or until > timezone.now():
            raise InvalidTimeRange("Since and/or until cannot be set to a future time")

    def get_incidents(self, team_id, since, until, offset=25):
        """
        Query all the incidents for a specific team

        :param team_id: (str) Team ID
        :param since: (str) Date in UTC to begin query
        :param until: (str) Date in UTC to end query
        :param offset: (int) Pagination offset

        :return: A generator of incidents
        """
        self._check_date(since, until)

        payload = {
            'team_ids[]': team_id,
            'time_zone': 'UTC',
            'since': since.isoformat(),
            'until': until.isoformat(),
            'offset': 0,
        }

        while True:
            incidents = self._query(method='GET', endpoint='incidents', payload=payload)

            yield incidents.get('incidents')

            payload['offset'] += offset

            if not incidents.get('more', False):
                return

    def get_incident(self, incident_id):
        """
        Get a specific incident

        :param incident_id: (str) Incident ID

        :return: (dict) incident details
        """
        return self._query(method='GET', endpoint=f'incidents/{incident_id}')

    def get_teams(self, offset=25):
        """
        Get a list of teams

        :param offset: (int) Pagination offset

        :return:
        """
        payload = {
            'offset': 0,
        }

        while True:
            teams = self._query(method='GET', endpoint='teams', payload=payload)

            yield teams.get('teams')

            payload['offset'] += offset

            if not teams.get('more', False):
                return

    def get_team(self, team_id):
        """
        Get a specific team

        :param team_id: (str) Team ID

        :return: (dict) Team
        """
        return self._query(method='GET', endpoint=f'teams/{team_id}')

    def get_schedules(self, team_id, offset=25):
        """
        Get a teams list of schedules

        :param team_id: (str) Team ID
        :param offset: (int) Pagination offset

        :return: (dict) A teams specific schedules
        """
        payload = {
            'offset': 0,
            'team_ids[]': team_id
        }

        while True:
            schedule = self._query(method='GET', endpoint='schedules', payload=payload)

            yield schedule.get('schedules')

            payload['offset'] += offset

            if not schedule.get('more', False):
                return

    def get_schedule(self, schedule_id, since, until):
        """
        Get a specific schedule with a finalized oncall

        :param schedule_id: (str) Schedule ID
        :param since: (str) The starting timestamp for the oncall schedule
        :param until: (str) The ending timestamp for the oncall schedule

        :return: (dict) Finalized oncall schedule
        """
        self._check_date(since, until)

        return self._query(
            method='GET',
            endpoint=f'schedules/{schedule_id}',
            payload={
                'id': schedule_id,
                'time_zone': 'UTC',
                'since': since.isoformat(),
                'until': until.isoformat(),
            }
        )
