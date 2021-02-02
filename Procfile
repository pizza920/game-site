release: chmod u+x release-tasks.sh && ./release-tasks.sh
web: python myapp/manage.py collectstatic --noinput; daphne pizzacade.asgi:application --port $PORT --bind 0.0.0.0 -v2