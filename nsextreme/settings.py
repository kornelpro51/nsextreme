# Django settings for nsextreme project.
import os
import socket


REALHOST = socket.gethostname()

HOSTNAME = socket.gethostname().lower().split('.')[0].replace('-', '')

DEVELOPMENT = True if HOSTNAME != 'nsxtest' else False

if DEVELOPMENT:
    DEBUG = True
else:
    DEBUG = True

FFMPEG_PATH = "/usr/local/bin/ffmpeg"

TEMPLATE_DEBUG = DEBUG
SITE_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

ADMINS = (
    ('Jordan Brant Baker', 'jbb@scryent.com'),
)

MANAGERS = ADMINS

if DEVELOPMENT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(SITE_ROOT, 'nsextreme.sqlite3'),
            'USER': '',                     # Not used with sqlite3.
            'PASSWORD': '',                 # Not used with sqlite3.
            'HOST': '',                     # Set to empty string for localhost.
            # Not used with sqlite3.
            'PORT': '',                     # Set to empty string for default.
            # Not used with sqlite3.
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(SITE_ROOT, 'nsextreme.sqlite3'),
            'USER': '',                     # Not used with sqlite3.
            'PASSWORD': '',                 # Not used with sqlite3.
            'HOST': '',                     # Set to empty string for localhost.
            # Not used with sqlite3.
            'PORT': '',                     # Set to empty string for default.
            # Not used with sqlite3.
            }
        }
    """
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'nsextreme',
            'USER': 'nsextreme',
            'PASSWORD': '99gagg$$!1',
            'HOST': 'localhost',
            }
        }
    """
# Email settings
if DEVELOPMENT:
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'nsextremewebaster123@gmail.com'
    EMAIL_HOST_PASSWORD = 'nsext123'
    #EMAIL_PORT = 1025
else:
    #EMAIL_HOST = 'localhost'
    #DEFAULT_FROM_EMAIL = "noreply@nsextreme.com"
    #EMAIL_PORT = 25
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'nsextremewebaster123@gmail.com'
    EMAIL_HOST_PASSWORD = 'nsext123'

###########################################
# block for django generic bookmark
#------------------------------------------
#
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
#TEMPLATE_CONTEXT_PROCESSORS += (
#     'nsextreme.context_processors.site',
#)
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'nsextreme.context_processors.site',
    'django_facebook.context_processors.facebook',
)
#GENERIC_BOOKMARKS_BACKEND = 'bookmarks.backends.MongoBackend'
#GENERIC_BOOKMARKS_MONGODB = {"NAME": "bookmarks"}
###########################################

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
if DEVELOPMENT:
    MEDIA_URL = 'http://localhost:8000/media/'
    SITE_URL = 'http://localhost:8000'
else:
    MEDIA_URL = 'http://nsxtest.nsextreme.com/media/'
    SITE_URL = 'http://nsxtest.nsextreme.com'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
if DEVELOPMENT:
    STATIC_URL = 'http://localhost:8000/static/'
else:
    STATIC_URL = 'http://nsxtest.nsextreme.com/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #STATIC_ROOT,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5rvk_^o*wpu3bjgovbzz0*e)+htmgf1s2ub@-btb)meetb_nv3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'hunger.middleware.BetaMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'nsextreme.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'nsextreme.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'nsextreme/templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'south',
    'registration',
    'registration_email',
    #'hunger',
    'bootstrap_toolkit',
    'debug_toolbar',
    'django_nose',
    'nsextreme',
    'app.userprofile',
    #'adzone'
    'django_facebook',
    'nsextreme.video'
)

# LOGGING

# - send an email to site admins on every HTTP 500 error when
#   DEBUG=False (Production/Staging)

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (
                '%(levelname)s %(asctime)s %(module)s %(process)d '
                '%(thread)d %(message)s')
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'NOTSET',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'logfile': {
            'level': 'NOTSET',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(SITE_ROOT, "debug.log"),
            'maxBytes': 50000,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'nsextreme': {
            'handlers': ['mail_admins', 'logfile'],
            'level': 'NOTSET',
            'filters': []
        }

    }
}

## registration
ACCOUNT_ACTIVATION_DAYS = 14

## BETA hunger
BETA_ENABLE_BETA = False
BETA_REDIRECT_URL = '/accounts/login/'
BETA_SIGNUP_ACCOUNT_URL = '/accounts/register/'
BETA_SIGNUP_URL = '/beta/'
BETA_ALWAYS_ALLOW_VIEWS = [
    'nsextreme.views.scanner',
    'nsextreme.api.urls.uploader'
]
BETA_SIGNUP_VIEWS = [
    'registration.views.register',
    'registration.views.activate',
    'django.views.generic.simple.direct_to_template'
]
BETA_SIGNUP_CONFIRMATION_URL = '/accounts/activate/complete/'

# DEBUGGING TOOLS

# debug-toolbar
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# nose for Django
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

AUTH_PROFILE_MODULE = 'nsextreme.UserProfile'

FACEBOOK_APP_ID = '285635568268467'
FACEBOOK_APP_SECRET = '3ca06688fd41db4a39ede10785e6e709'

FACEBOOK_REGISTRATION_BACKEND = 'registration.backends.default.DefaultBackend'

ACCOUNT_ACTIVATION_DAYS = 7

AUTHENTICATION_BACKENDS = {
    'django_facebook.auth_backends.FacebookBackend',
    'registration_email.auth.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
}
#REGISTRATION_EMAIL_ACTIVATE_SUCCESS_URL = '/accounts/activate/complete/'
#REGISTRATION_EMAIL_REGISTER_SUCCESS_URL = '/accounts/register/complete/'