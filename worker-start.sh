#! /usr/bin/env bash
set -e

hatch run celery -A app.services.celery worker -l info -Q rag -c 1
