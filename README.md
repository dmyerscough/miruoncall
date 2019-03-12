Miruoncall
==========

Oncall dashboard that is used for handovers.

# Celery

## Configure celery beat

Configure celery beat to run scheduled periodic tasks

```bash
DJANGO_SETTINGS_MODULE='miruoncall.settings.testing' celery -A miruoncall beat -l debug --max-interval 60
```

## Configure celery workers

Configure celery worker to execute beat tasks

```bash
DJANGO_SETTINGS_MODULE='miruoncall.settings.testing' celery -A miruoncall worker -l debug
```

# API

## Query Incidents

Query all incidents for the `88e406ab39e04d7bb92b8ca2bd4cff98` team

```bash
$ curl -s -X GET -H "Content-Type: application/json" -d '{"since": "2018-12-20", "until": "2018-12-30"}' http://127.0.0.1:8000/incidents/88e406ab39e04d7bb92b8ca2bd4cff98  | jq .
{
  "incidents": [
    {
      "title": "Blat 26",
      "description": "Blat 26",
      "summary": "[#27] Blat 26",
      "status": "resolved",
      "actionable": true,
      "created_at": "2018-12-26T09:04:41Z",
      "incident_id": "PS2NK9B",
      "annotation": null,
      "urgency": "high"
    },
    ...
    ...
    ...
    {
      "title": "Down Master DB",
      "description": "Down Master DB",
      "summary": "[#1] Down Master DB",
      "status": "resolved",
      "actionable": true,
      "created_at": "2018-12-24T07:13:38Z",
      "incident_id": "PZEUF78",
      "annotation": null,
      "urgency": "high"
    }
  ],
  "incident_count": {
    "2018-12-26": 26,
    "2018-12-24": 1
  }
}
```

## Create an annotation for an incident

Create an annotation for the incident `3cec1b1c-9fa5-4943-baec-b81c65b801b1`

```bash
$ curl -s -X POST -H "Content-Type: application/json" -d '{"incident_ids": "3cec1b1c-9fa5-4943-baec-b81c65b801b1", "annotation": "This is a simple annotation", "actionable": true}' http://127.0.0.1:8000/incidents/88e406ab39e04d7bb92b8ca2bd4cff98
```

Only update the incident to specify if the incident was actionable

```bash
$ curl -s -X POST -H "Content-Type: application/json" -d '{"actionable": true}' http://127.0.0.1:8000/incidents/88e406ab39e04d7bb92b8ca2bd4cff98
```

# Building Docker Image

```bash
$ docker build -t quay.io/dmyerscough/miruoncall:0.0.1 .
$ docker push quay.io/dmyerscough/miruoncall:0.0.1
```

## Deployment

Template out the deployment using Helm

```bash
helm template miruoncall --name miruoncall --set application.django_secret_key="XXXX" --set application.pagerduty="XXXX"
```

# Deploy Celerybeat

```bash
helm template miruoncall --name celerybeat --set application.celerybeat.enabled=true
```

# Deploy Celery Worker

```bash
helm template miruoncall --name celery --set application.celery.enabled=true
```