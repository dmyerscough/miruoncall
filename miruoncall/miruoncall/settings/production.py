"""
Django settings for miruoncall project.
"""

from .base import *  # noqa

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')  # noqa

DEBUG = False
ALLOWED_HOSTS = ["oncall.mirulabs.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE'),  # noqa
        'USER': os.getenv('DATABASE_USERNAME'),  # noqa
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),  # noqa
        'HOST': os.getenv('DATABASE_HOSTNAME'),  # noqa
        'OPTIONS': {
            'sslmode': 'require',
            'sslrootcert': os.getenv('ROOT_CERT'),  # noqa
            'sslcert': os.getenv('SSL_CERT'),  # noqa
            'sslkey': os.getenv('SSL_KEY'),  # noqa
        },
    },
}
