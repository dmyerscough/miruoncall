# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime, timedelta

from .models import Incidents, Team
from .pagerduty import PagerDuty

logger = logging.getLogger(__name__)


def populate_alerts(team, since, until):
    """
    Populate team alerts

    :param team: PagerDuty Team ID
    :param since:
    :param until:

    :return: (bool) successful
    """
    pyduty = PagerDuty(os.getenv('PAGERDUTY_KEY', 'ujgvDDjLwhLSG2XaoRAj'))

    # since = datetime.utcnow() - timedelta(days=7)
    # until = datetime.utcnow()

    for incidents in pyduty.get_incidents(team_id=team.team_id, since=since, until=until):
        for incident in incidents:
            _, created = Incidents.objects.get_or_create(
                title=incident['title'],
                description=incident['description'],
                summary=incident['summary'],
                status=incident['status'],
                created_at=incident['created_at'],
                incident_id=incident['id'],
                urgency=incident['urgency'],
                team=team,
            )

            if created:
                logger.info(f"{incident['id']} has been created")

    return True


def populate_teams():
    """
    Populate team details
    """
    pyduty = PagerDuty(os.getenv('PAGERDUTY_KEY', 'ujgvDDjLwhLSG2XaoRAj'))

    for teams in pyduty.get_teams():
        for team in teams:
            _, created = Team.objects.get_or_create(
                name=team['name'],
                team_id=team['id'],
                summary=team['summary'],
            )

            if created:
                logger.info(f"{team['name']} has been created")

    return True
