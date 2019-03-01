# -*- coding: utf-8 -*-

import logging
import os
from datetime import timedelta

import dateutil.parser
from django.conf import settings
from django.utils import timezone

from miruoncall.celery import app as celery_app
from oncall.models import Incidents, Team
from oncall.pagerduty import PagerDuty, RequestFailure

logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def populate_alerts(self):
    """
    Trigger a celery job for each team to populate alerts
    """
    until = timezone.now()

    for team in Team.objects.all():
        _populate_alerts.delay(team_id=team.id, since=team.last_checked, until=until)

    return True


@celery_app.task(bind=True, autoretry_for=(Exception,), exponential_backoff=2, retry_kwargs={'max_retries': 3}, retry_jitter=False)
def _populate_alerts(self, team_id, since, until):
    """
    Populate team alerts

    :param team: PagerDuty Team ID
    :param since:
    :param until:

    :return: (bool) successful
    """
    pyduty = PagerDuty(os.getenv('PAGERDUTY_KEY'))

    team = Team.objects.get(id=team_id)

    try:
        for incidents in pyduty.get_incidents(team_id=team.team_id, since=dateutil.parser.parse(since), until=dateutil.parser.parse(until)):
            for incident in incidents:
                _, created = Incidents.objects.get_or_create(
                    title=incident.get('title', 'No title'),
                    description=incident.get('description', 'No description'),
                    summary=incident.get('summary', 'No summary'),
                    status=incident.get('status', 'No status'),
                    created_at=incident['created_at'],
                    incident_id=incident['id'],
                    urgency=incident['urgency'],
                    team=team,
                )

                if created:
                    logger.info(f"{incident['id']} has been created")
    except RequestFailure as err:
        logger.error(f'Failed to query PagerDuty: {err}')

        return False

    team.save()

    return True


@celery_app.task(bind=True, autoretry_for=(Exception,), exponential_backoff=2, retry_kwargs={'max_retries': 3}, retry_jitter=False)
def populate_teams(self):
    """
    Populate team details
    """
    pyduty = PagerDuty(os.getenv('PAGERDUTY_KEY'))

    try:
        for teams in pyduty.get_teams():
            for team in teams:
                team_, created = Team.objects.get_or_create(
                    name=team['name'],
                    team_id=team['id'],
                    summary=team['summary'],
                )

                if created:
                    logger.info(f"{team['name']} has been created")

                    if settings.INITIAL_INCIDENT_LOOKBACK is not None:
                        # When the team bootstrap occurs query the past X days for incidents
                        Team.objects.filter(id=team_.id).update(
                            last_checked=team_.last_checked - timedelta(days=int(settings.INITIAL_INCIDENT_LOOKBACK))
                        )

    except RequestFailure as err:
        logger.error(f'Failed to query PagerDuty: {err}')

        return False

    return True


@celery_app.task(bind=True)
def update_incidents(self):
    """
    Check the status on unresolved tickets
    """
    for incident in Incidents.objects.all().exclude(status='resolved'):
        _update_incident.delay(incident_id=incident.id)

    return True


@celery_app.task(bind=True, autoretry_for=(Exception,), exponential_backoff=2, retry_kwargs={'max_retries': 3}, retry_jitter=False)
def _update_incident(self, incident_id):
    """
    Check the status of a ticket and update the status
    """
    pyduty = PagerDuty(os.getenv('PAGERDUTY_KEY'))

    incident = Incidents.objects.get(id=incident_id)
    resp = pyduty.get_incident(incident_id=incident.incident_id)

    if resp['status'] != incident.status:
        logger.info(f'Updated incident {incident.incident_id} with the new status of {resp["status"]}')

        incident.status = resp['status']
        incident.save()

    return True
