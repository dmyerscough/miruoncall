# -*- coding: utf-8 -*-

import logging
from datetime import timedelta

import dateutil.parser as dtparse
import pytz
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from oncall.models import Annotations, Incidents, Team
from oncall.serializer import IncidentSerializer

logger = logging.getLogger(__name__)


class Oncall(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, team_id):
        """
        List all incidents for a specific time frame
        """
        incident_count_by_day = {}

        try:
            since = dtparse.parse(request.data.get('since', request.GET.get('since', (timezone.now() - timedelta(days=7)).isoformat())))
            until = dtparse.parse(request.data.get('until', request.GET.get('until', timezone.now().isoformat())))
        except ValueError:
            return JsonResponse({'error': 'Invalid date format YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        if since > until:
            return JsonResponse({'error': 'since cannot be newer than until'}, status=status.HTTP_400_BAD_REQUEST)

        if not Team.objects.filter(id=team_id).exists():
            return JsonResponse({'error': f'{team_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        incidents = Incidents.objects.filter(
            created_at__range=[since.replace(tzinfo=pytz.UTC), until.replace(tzinfo=pytz.UTC)], team__id=team_id
        ).order_by('-created_at')

        for incident in incidents:
            incident_count_by_day.setdefault(incident.created_at.strftime('%Y-%m-%d'), 0)
            incident_count_by_day[incident.created_at.strftime('%Y-%m-%d')] += 1

        return JsonResponse(
            {
                'incidents': IncidentSerializer(incidents, many=True).data,
                'incident_count': incident_count_by_day,
            }, status=status.HTTP_200_OK
        )

    def post(self, request, team_id):
        """
        Update one or multiple incidents with annotations
        """
        incident_ids = request.data.get('incident_ids', request.GET.get('incident_ids'))
        annotation_message = request.data.get('annotation', request.GET.get('annotation'))
        actionable = request.data.get('actionable', request.GET.get('actionable'))

        if incident_ids is None:
            return JsonResponse({'error': 'incident_ids is a required argument'}, status=status.HTTP_400_BAD_REQUEST)

        if not Team.objects.filter(id=team_id).exists():
            return JsonResponse({'error': f'{team_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if annotation_message is not None:
            annotation, _ = Annotations.objects.get_or_create(
                annotation=annotation_message,
            )

        for incident_id in incident_ids.replace(' ', '').split(','):
            try:
                incident = Incidents.objects.get(id=incident_id, team__id=team_id)

                if annotation_message is not None:
                    incident.annotation = annotation

                if actionable is not None:
                    incident.actionable = actionable

                incident.save()
            except (ValueError, ValidationError):
                logger.error(f'Invalid incident id: {incident_id}')

                return JsonResponse({'error': f'Invalid incident id: {incident_id}'}, status=status.HTTP_400_BAD_REQUEST)
            except Incidents.DoesNotExist:
                logger.error(f'Incident {incident_id} does not exist')

                return JsonResponse({'error': f'Incident {incident_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'message': 'successfully updated'}, status=status.HTTP_200_OK)
