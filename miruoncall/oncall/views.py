# -*- coding: utf-8 -*-

from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class Oncall(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        pass

    def post(self, request):
        pass

    def delete(self, request):
        pass
