Miruoncall
==========




### Configure celery beat

Configure celery beat to run scheduled periodic tasks

```bash
DJANGO_SETTINGS_MODULE='miruoncall.settings.testing' celery -A miruoncall beat -l debug --max-interval 60
```

### Configure celery workers

Configure celery worker to execute beat tasks

```bash
DJANGO_SETTINGS_MODULE='miruoncall.settings.testing' celery -A miruoncall worker -l debug
```