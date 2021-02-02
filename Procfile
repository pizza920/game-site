release: chmod u+x release-tasks.sh && ./release-tasks.sh
web: python3 manage.py collectstatic; daphne pizzacade.asgi:application --port $PORT --bind 0.0.0.0 -v2