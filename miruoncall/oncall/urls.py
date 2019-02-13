# -*- coding: utf-8 -*-

from django.urls import path

from oncall.views import Oncall, Teams

urlpatterns = [
    path('incidents/<team_id>/', Oncall.as_view(), name='incidents'),
    path('teams/', Teams.as_view(), name='teams'),
]
