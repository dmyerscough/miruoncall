# -*- coding: utf-8 -*-

from rest_framework import serializers

from oncall.models import Incidents


class IncidentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Incidents

        fields = ("title", "description", "summary", "status", "actionable", "created_at", "incident_id", "annotation", "urgency")
