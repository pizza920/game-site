release: python3 pizzacade/manage.py makemigrations
release: python3 pizzacade/manage.py migrate
web: gunicorn --pythonpath pizzacade pizzacade.wsgi