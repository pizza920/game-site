print("DEV SETTINGS ENABLED")

from .settings_common import *

INSTALLED_APPS_DEV = ['whitenoise.runserver_nostatic']
INSTALLED_APPS = INSTALLED_APPS_DEV + INSTALLED_APPS

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}