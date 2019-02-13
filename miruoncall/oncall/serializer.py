# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from rest_framework import serializers

from oncall.models import Annotations, Incidents, Team


class AnnotationSerializer(serializers.ModelSerializer):

    created_by = serializers.CharField(source='created_by.username')

    class Meta:
        model = Annotations

        fields = ('annotation', 'created_at', 'created_by')


class IncidentSerializer(serializers.ModelSerializer):

    annotation = AnnotationSerializer(many=False)

    class Meta:
        model = Incidents

        fields = ('id', 'title', 'description', 'summary', 'status', 'actionable', 'created_at', 'incident_id', 'annotation', 'urgency')


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team

        fields = ('id', 'name')
