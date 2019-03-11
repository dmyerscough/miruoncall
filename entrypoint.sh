#!/bin/bash

start_webapp() {
    echo "Starting Gunicorn"
    exec gunicorn miruoncall.wsgi:application \
        --name miruoncall \
        --workers 5 \
        --bind=unix:/webapp/run/gunicorn.sock \
        --log-level=info \
        --log-file=/webapp/logs/gunicorn.log \
        --access-logfile=/webapp/logs/gunicorn-access.log \
        --error-logfile=/webapp/logs/gunicorn-error.log &

    echo "Starting Nginx"
    exec nginx -g "daemon off;"
}

start_celery_worker() {
    echo "Starting celery worker"
    exec celery -A miruoncall worker -l info -n worker1@%h -c 5
}

start_celery_beat() {
    echo "Starting celery beat"
    exec celery -A miruoncall beat -l info --max-interval 60
}

if [[ ${CELERY_WORKER} = true ]]; then
    start_celery_worker
elif [[ ${CELERYBEAT} = true ]]; then
    start_celery_beat
else
    start_webapp
fi
