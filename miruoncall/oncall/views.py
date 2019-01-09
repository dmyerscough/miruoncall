# -*- coding: utf-8 -*-

from datetime import timedelta

from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from oncall.models import Incidents


class Oncall(APIView):

    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        """

        :param request:

        :return:
        """
        try:
            since = request.data.get('since', (timezone.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
            until = request.data.get('until', timezone.now().strftime('%Y-%m-%d'))
        except ValueError:
            return JsonResponse({'error': 'Invalid date format YYYY/MM/DD'}, status=status.HTTP_400_BAD_REQUEST)

        incidents = Incidents.objects.filter(created_at__range=[since, until])

        return JsonResponse({'incidents': 1}, status=status.HTTP_200_OK)

    def post(self, request):
        pass

    def delete(self, request):
        pass
