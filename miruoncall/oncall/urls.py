# -*- coding: utf-8 -*-

from django.urls import path

from oncall.views import Incident, Oncall, Teams

urlpatterns = [
    path('incident/<team_id>/<incident_id>/', Incident.as_view(), name="incident"),
    path('incidents/<team_id>/', Oncall.as_view(), name='incidents'),
    path('teams/', Teams.as_view(), name='teams'),
]
