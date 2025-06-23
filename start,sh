#!/usr/bin/env bash
set -e

if [ "$1" = 'uwsgi' ]; then
    # # Experimental: use gosu to run uwsgi as a specific user
    # USER_ID=`id -u`
    # GROUP_ID=`id -g`
    # if [ ! -z "$2" ]; then
    #     USER_ID="$2"
    # fi
    # if [ ! -z "$3" ]; then
    #     GROUP_ID="$3"
    # fi
    # exec gosu admin uwsgi --http=0.0.0.0:80 --module=prj.wsgi --die-on-term --uid "${USER_ID}" --gid "${GROUP_ID}"
    exec uwsgi --http=0.0.0.0:80 --module=prj.wsgi --die-on-term --touch-reload=/app/uwsgi.reload
fi

exec "$@"
