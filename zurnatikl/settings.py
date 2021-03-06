"""
Django settings for zurnatikl project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition

INSTALLED_APPS = [
    'django_admin_bootstrapped',
    #### default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    #### local dependencies
    'ajax_select',
    'eultheme',
    'downtime',      # required by eultheme even if we aren't using it
    'widget_tweaks',
    'stdimage',
    #### local apps
    'zurnatikl.apps.admin',
    'zurnatikl.apps.geo',
    'zurnatikl.apps.people',
    'zurnatikl.apps.journals',
    'zurnatikl.apps.network',
    'zurnatikl.apps.content',
    # uncomment in your greatest time of need!
    # (migrating partial data from one DB to another, hopefully we never
    # need this again)
    #'fixture_magic',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(BASE_DIR, 'templates')
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors' :[
                    # Default processors##############################
                    "django.contrib.auth.context_processors.auth",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.media",
                    "django.template.context_processors.static",
                    "django.template.context_processors.tz",
                    "django.contrib.messages.context_processors.messages",
                    ##################################################
                    "django.template.context_processors.request",
                    "eultheme.context_processors.template_settings",
                    "eultheme.context_processors.downtime_context",
                    ### local context processors
                    "zurnatikl.version_context",
                    "zurnatikl.apps.journals.context_processors.search",
                    "zurnatikl.apps.content.context_processors.banner_image",
                ],
                'debug': True,
            }
        }
]


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'eultheme.middleware.DownpageMiddleware',
)

ROOT_URLCONF = 'zurnatikl.urls'

WSGI_APPLICATION = 'zurnatikl.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'sitemedia'),
]

MEDIA_URL = '/media/'


# used with admin_reorder template tag
ADMIN_REORDER = (
    ("auth", ('Group', 'User')),
    ("geo", ('Location')),
    ("people", ('Person', 'School')),
    ("journals", ('Journal', 'Issue', 'IssueItem', 'Genre'))
)

# lookup channels for ajax autocompletes on the site
AJAX_LOOKUP_CHANNELS = {
    #  simple: search Person.objects.filter(name__icontains=q)
    # custom lookup channel to allow searching on multiple fields
    'location' : ('zurnatikl.apps.geo.lookups', 'LocationLookup'),
    'person' : ('zurnatikl.apps.people.lookups', 'PersonLookup')
}


# import localsettings
# This will override any previously set value
try:
    from localsettings import *
except ImportError:
    import sys
    print >> sys.stderr, '''Settings not defined. Please configure a version
        of localsettings.py for this site. See localsettings.py.dist for
        setup details.'''

# enable django-debug-toolbar if installed
try:
    import debug_toolbar
    # FIXME: not working at the moment, ignoring for now
    # INSTALLED_APPS.append('debug_toolbar')
except ImportError:
    pass

# load & configure django_nose if available (only needed for development)
try:
    # NOTE: errors if DATABASES is not configured (in some cases),
    # so this must be done after importing localsettings
    import django_nose
    INSTALLED_APPS.append('django_nose')
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    # enable coverage by default
    NOSE_ARGS = [
        # '--with-coverage',
        '--cover-package=zurnatikl',
    ]
except ImportError:
    pass
