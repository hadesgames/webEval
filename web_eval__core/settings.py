# Django settings for webEval project.

import os
from django.core.urlresolvers import reverse

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG
HOST_URL  = 'http://localhost:8000'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db.sql',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Bucharest'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'public', 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/'.join(['', 'static'])

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*t!p!h2z!w*09xl00(hukx5+kl%4o^m=&+pj$yxuyrxo-6j$gu'

# Make this unique, and don't share it with anybody.

if not hasattr(globals(), 'SECRET_KEY'):
    SECRET_FILE = os.path.join(PROJECT_ROOT, 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            from random import choice
            import string
            symbols = ''.join((string.lowercase, string.digits, string.punctuation ))
            SECRET_KEY = ''.join([choice(symbols) for i in range(50)])
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            raise Exception('Please create a %s file with random characters to generate your secret key!' % SECRET_FILE)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
   # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    #'django_authopenid.middleware.OpenIDMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
   # "socialauth.context_processors.facebook_api_key",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    
    'django.core.context_processors.media',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
)

LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = '/auth/successful-login/'
LOGOUT_URL = '/auth/logout/'
OPENID_SSO_SERVER_URL = 'https://www.google.com/accounts/o8/id'

ROOT_URLCONF = 'webEval.urls'
STATIC_DOC_ROOT = os.path.join(os.path.dirname(__file__), 'public', 'static')
ATTACHMENTS_DIR = os.path.join(os.path.dirname(__file__), 'files', 'attachments')
JOBS_DIR = os.path.join(os.path.dirname(__file__), 'files', 'jobs')
AVATARS_DIR = os.path.join(os.path.dirname(__file__), 'public', 'static', 'images', 'avatar')
EVAL_DIR = os.path.join(os.path.dirname(__file__), '..', 'eval')

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'public', 'html')
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


from config import akismet, reCaptcha
from config import facebook as facebook_config
from config import gmail as gmail_config
from config import twitter as twitter_config

CUSTOM_USER_MODEL = 'webEval.web_eval__core.user__model.UserProfile'

AKISMET_API_KEY = akismet.AKISMET_API_KEY
RECAPTCHA_PUBLIC_KEY = reCaptcha.RECAPTCHA_PUBLIC_KEY
RECAPTCHA_PRIVATE_KEY = reCaptcha.RECAPTCHA_PRIVATE_KEY

EMAIL_USE_TLS = gmail_config.EMAIL_USE_TLS
EMAIL_HOST = gmail_config.EMAIL_HOST
EMAIL_HOST_USER = gmail_config.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = gmail_config.EMAIL_HOST_PASSWORD
EMAIL_PORT = gmail_config.EMAIL_PORT

FACEBOOK_APP_ID = facebook_config.FACEBOOK_APP_ID
FACEBOOK_API_KEY =  facebook_config.FACEBOOK_API_KEY
FACEBOOK_API_SECRET = facebook_config.FACEBOOK_API_SECRET
FACEBOOK_REDIRECT_URI = facebook_config.FACEBOOK_REDIRECT_URI

CONSUMER_KEY = twitter_config.CONSUMER_KEY
CONSUMER_SECRET = twitter_config.CONSUMER_SECRET

OAUTH_AUTH_VIEW = "piston.authentication.oauth_auth_view"
OAUTH_CALLBACK_VIEW = "piston.authentication.oauth_user_auth"

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'webEval.auth_backend.FacebookBackend',
    'webEval.auth_backend.GoogleBackend',
    'webEval.auth_backend.TwitterBackend',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django_extensions',
    'django_openid_auth',
    'captcha',
    'pagination',
    'piston',
    'south',
    'web_eval__core',
)

