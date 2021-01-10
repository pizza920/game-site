release: chmod u+x release-tasks.sh && ./release-tasks.sh
web:cd pizzacade && daphne --pythonpath pizzacade.asgi:application --port $PORT --bind 0.0.0.0 -v2