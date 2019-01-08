"""
Django settings for miruoncall project.
"""

from .base import *  # noqa

SECRET_KEY = 'g=2=7k&#72^0*=*9si69^#pt10x&q-4+2wu1)orrrt5y+gzxf!'

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # noqa
    }
}

THIRD_PARTY_DEBUG_APPS = (
    'debug_toolbar',
    'django_extensions',
    'django_nose',
)

INSTALLED_APPS += THIRD_PARTY_DEBUG_APPS  # noqa

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=oncall',
    '--cover-html',
    '--cover-inclusive',
    '--verbosity=3'
]

MIDDLEWARE.append(  # noqa
    'debug_toolbar.middleware.DebugToolbarMiddleware'
)

INTERNAL_IPS = '127.0.0.1'
