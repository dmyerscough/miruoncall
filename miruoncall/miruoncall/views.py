# -*- coding: utf-8 -*-

from django.http import JsonResponse
from rest_framework import status


def healthz(request):
    """
    Return a simple health check
    """
    return JsonResponse({'status': 'OK'}, status=status.HTTP_200_OK)
