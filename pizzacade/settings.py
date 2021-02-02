print("PROD SETTINGS ENABLED")

from .settings_common import *
import dj_database_url


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com', 'pizzacade.com']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'channels',
    'games',
    # 'cloudinary',
]

# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': 'YOUR_CLOUD_NAME',
#     'API_KEY': 'YOUR_API_KEY',
#     'API_SECRET': 'YOUR_API_SECRET',
# }
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
