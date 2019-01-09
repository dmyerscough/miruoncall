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

        TODO: Check the since date is not greater than the until date

        :param request:

        :return:
        """
        try:
            since = dateutil.parser.parse(request.data.get('since', (timezone.now() - timedelta(days=7)).isoformat()))
            until = dateutil.parser.parse(request.data.get('until', timezone.now().isoformat()))
        except ValueError:
            return JsonResponse({'error': 'Invalid date format YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        incidents = Incidents.objects.filter(
            created_at__range=[since.replace(tzinfo=pytz.UTC), until.replace(tzinfo=pytz.UTC)]
        )

        return JsonResponse(
            {'incidents': IncidentSerializer(incidents, many=True).data}, status=status.HTTP_200_OK
        )

    def post(self, request):
        pass

    def delete(self, request):
        pass
