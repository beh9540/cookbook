'''
Created on Mar 12, 2013

Contains settings for development testing

@author: bhowell
'''
from django.conf import settings

DEBUG = True

INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('Test Admin', 'test@example.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cookbook',                      # Or path to database file if using sqlite3.
        'USER': 'cookbook',                      # Not used with sqlite3.
        'PASSWORD': 'cookbook',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
             
}

settings.INSTALLED_APPS += ('debug_toolbar', )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'root': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

