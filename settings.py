import os
_base = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    #('admin', 'application.testbed@gmail.com'),
    ('panuta', 'panuta@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'plm_dev'
DATABASE_USER = 'plm_dev'
DATABASE_PASSWORD = 'plm_dev'
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'Asia/Bangkok'
LANGUAGE_CODE = 'th'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.path.join(_base, "media") + "/"
MEDIA_URL = '/m'
ADMIN_MEDIA_PREFIX = '/media/'

AUTH_PROFILE_MODULE = 'accounts.UserAccount'
ACCOUNT_ACTIVATION_DAYS = 3
LOGIN_REDIRECT_URL = "/dashboard/"

WEBSITE_ADDRESS = 'localhost:8000'

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
    'thaihealthplm.administration',
    'thaihealthplm.domain',
    'thaihealthplm.helper',
    'thaihealthplm.budget',
    'thaihealthplm.progress',
    'thaihealthplm.kpi',
    
    'registration',
)

# ================================================================ #
# ========================= PLM Settings ========================= #

QUARTER_START_MONTH = 10 # (1 is for January)
# IMPORTANT NOTE! Not support quarter which start and end of quarter is in different year

QUARTER_LOWER_YEAR_NUMBER = False # Use lower year number to represent if QUARTER_START_MONTH is not 1
QUARTER_INPUT_YEAR_SPAN = 5





