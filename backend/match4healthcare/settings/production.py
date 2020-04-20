from match4healthcare.settings.common import *
from django.utils.log import DEFAULT_LOGGING
import logging

DEFAULT_LOGGING['handlers']['console']['filters'] = []

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['matchmedisvsvirus.dynalias.org', 'helping-health.from-de.com', 'match4healthcare.de',
                 'match4healthcare.eu', 'match4healthcare.org', 'medis-vs-covid19.de', 'localhost']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', ''),
        'USER': os.environ.get('POSTGRES_USER', ''),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': 'database',
        'PORT': '5432',
    }
}

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =============== MAIL RELAY SERVER CONFIGURATION ===============
# ToDo add environment variable based detection whether we are on prod or staging
NOREPLY_MAIL = 'match4healthcare<noreply@match4healthcare.de>'
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

# Use API instead of SMTP server
use_sendgrid_api = True

if use_sendgrid_api:
    # Using the API
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

    # Disable all tracking options
    SENDGRID_TRACK_EMAIL_OPENS = False
    SENDGRID_TRACK_CLICKS_HTML = False
    SENDGRID_TRACK_CLICKS_PLAIN = False

else:
    # Normal SMTP
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = 'apikey'
    EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True


WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': True,
        'BUNDLE_DIR_NAME': '/', # must end with slash
        'STATS_FILE': os.path.normpath(os.path.join(os.path.join(os.path.dirname(BASE_DIR),'frontend'),'webpack-stats.json')),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        #'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
        'LOADER_CLASS': 'webpack_loader.loader.WebpackLoader',
    }
}
