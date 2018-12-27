
import uuid

from django.db import models


class Annotations(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    annotation = models.TextField(max_length=255)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.annotation}"


class Incidents(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.TextField(max_length=25)
    description = models.TextField(max_length=100)

    status = models.TextField(max_length=12)

    actionable = models.BooleanField(default=True)
    created_at = models.DateTimeField()

    incident_id = models.TextField(max_length=20, unique=True)
    triggered = models.DateTimeField()

    annotation = models.ForeignKey(Annotations, on_delete=False)

    urgency = models.TextField()

    def __str__(self):
        return f"{self.incident_id}"


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    team = models.TextField()
    schedule = models.TextField()

    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.team}"
