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
