
import uuid

from django.contrib.auth.models import User
from django.db import models


class Annotations(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    annotation = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.annotation}"


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.TextField()
    team_id = models.TextField()

    summary = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_checked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Incidents(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.TextField(max_length=25)
    description = models.TextField(max_length=100)
    summary = models.TextField(max_length=100)

    status = models.TextField(max_length=12)

    actionable = models.BooleanField(default=True)
    created_at = models.DateTimeField()

    incident_id = models.TextField(max_length=20, unique=True)

    annotation = models.ForeignKey(Annotations, on_delete=False, blank=True, null=True)

    urgency = models.TextField(max_length=15)

    team = models.ForeignKey('Team', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.incident_id}"
