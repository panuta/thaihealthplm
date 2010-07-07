import os
_base = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'plm_dev'             # Or path to database file if using sqlite3.
DATABASE_USER = 'plm_dev'             # Not used with sqlite3.
DATABASE_PASSWORD = 'plm_dev'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'Asia/Bangkok'
LANGUAGE_CODE = 'th'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.path.join(_base, "media") + "/"
MEDIA_URL = '/m'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

AUTH_PROFILE_MODULE = 'accounts.UserAccount'
ACCOUNT_ACTIVATION_DAYS = 3
LOGIN_REDIRECT_URL = "/dashboard/"

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'application.testbed@gmail.com'
EMAIL_HOST_PASSWORD = 'opendream'
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = '[SMS] '

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$xxc1&yf9@#r%wm#4i+=w3es1v3$m(nrdx0v(bm=zim^a93l@t'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    #"thaihealthsms.context_processors.user_account",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'thaihealthplm.urls'

TEMPLATE_DIRS = (
    os.path.join(_base, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    
    'thaihealthplm.accounts',
    'thaihealthplm.domain',
    'thaihealthplm.budget',
    'thaihealthplm.progress',
    'thaihealthplm.kpi',
    
    'registration',
)
