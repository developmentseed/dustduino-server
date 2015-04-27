"""
Django settings for sensor project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join, dirname

from configurations import Configuration, values

BASE_DIR = dirname(dirname(__file__))


class Base(Configuration):

    BASE_DIR = BASE_DIR

    PORTAL_URL = values.Value('http://127.0.0.1:8000')

    INSTALLED_APPS = (
        'django.contrib.admin',
        'corsheaders',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'rest_framework.authtoken',
        'api',
        'sensors',
        'finalware',
    )

    # See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

    SECRET_KEY = 'CHANGEME!!!'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)
    TEMPLATE_DEBUG = DEBUG

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'urls'

    WSGI_APPLICATION = 'wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/1.7/ref/settings/#databases

    DATABASES = values.DatabaseURLValue('sqlite:///%s' % join(BASE_DIR, 'db.sqlite3'))

    # Internationalization
    # https://docs.djangoproject.com/en/1.7/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # EMAIL CONFIGURATION
    EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')
    DEFAULT_FROM_EMAIL = values.Value('Sensor API <noreply@example.com>')
    # END EMAIL CONFIGURATION

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.7/howto/static-files/
    STATIC_ROOT = join(os.path.dirname(BASE_DIR), 'staticfiles')
    STATIC_URL = '/static/'

    # Django CORS

    CORS_ORIGIN_ALLOW_ALL = values.BooleanValue(True)
    CORS_URLS_REGEX = r'^/v[0-9]/.*$'
    CORS_ALLOW_METHODS = (
        'GET',
        'POST',
        'PUT',
    )
    # End Django CORS
