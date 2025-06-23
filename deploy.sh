#!/usr/bin/env bash
set -e
set -x

git pull

docker compose build

docker compose up -d

docker compose exec web python manage.py migrate --noinput

docker compose exec web python manage.py collectstatic --noinput

docker compose exec web touch /app/uwsgi.reload
