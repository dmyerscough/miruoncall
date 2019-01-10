# -*- coding: utf-8 -*-

from datetime import timedelta

import dateutil.parser
import pytz
from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from oncall.models import Incidents
from oncall.serializer import IncidentSerializer


class Oncall(APIView):

    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        List all incidents
        """
        incident_count_by_day = {}

        try:
            since = dateutil.parser.parse(request.data.get('since', (timezone.now() - timedelta(days=7)).isoformat()))
            until = dateutil.parser.parse(request.data.get('until', timezone.now().isoformat()))
        except ValueError:
            return JsonResponse({'error': 'Invalid date format YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        if since > until:
            return JsonResponse({'error': 'Since cannot be newer than until'}, status=status.HTTP_400_BAD_REQUEST)

        incidents = Incidents.objects.filter(
            created_at__range=[since.replace(tzinfo=pytz.UTC), until.replace(tzinfo=pytz.UTC)]
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

    def post(self, request):
        pass

    def delete(self, request):
        pass
