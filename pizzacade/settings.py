print("PROD SETTINGS ENABLED")

from .settings_common import *
import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
    'cloudinary',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# django_on_heroku.settings(locals())

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
SSTATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#
# # Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'games/static'),
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'hxuie33uy',
    'API_KEY': '839277731853354',
    'API_SECRET': 'Y3N5HLgMod99iBz64J9RkU2LRzQ',
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
