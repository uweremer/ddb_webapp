"""
Django settings for ddb_webapp project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import posixpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists(os.path.join(BASE_DIR, '.credentials')):
    with open(os.path.join(BASE_DIR, 'test_credentials.txt')) as f:
        CRED = f.read().splitlines() 

if os.path.exists(os.path.join(BASE_DIR, '.credentials')):	
    with open(os.path.join(BASE_DIR, '.credentials')) as f:
        CRED = f.read().splitlines() 

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CRED[2]

if CRED[1] == 'development':
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']
    INTERNAL_IPS = ['127.0.0.1',]

    # EMails are redirected to file
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH =  'email_devel_inbox'


if CRED[1] != 'development':
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False
    ALLOWED_HOSTS = ['beteiligungslandschaft-bw.de', 'www.beteiligungslandschaft-bw.de']

    # Session Cookies and SSL
    # Documentation: https://docs.djangoproject.com/en/2.2/ref/settings/#sessions
    #SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    #SESSION_COOKIE_HTTPONLY = True #Javascript kann nicht auf Cookies zugreifen
    #SESSION_COOKIE_SECURE = True #Session cookie only send over https connection geschickt
    #CSRF_COOKIE_SECURE = True
    #SECURE_SSL_REDIRECT  = True




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    # Own Apps
    'baseapp',
    'basisdaten',
    'ddb_showcase',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware',] + MIDDLEWARE


ROOT_URLCONF = 'ddb_webapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'baseapp.context_processors.constant_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'ddb_webapp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': CRED[4],
        'USER': CRED[5],
        'PASSWORD': CRED[6],
        'HOST': 'localhost',
        'PORT': '',
    },
}


#Whoosh Search Backend
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "deploy", "static_files")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL='/media/'

MEDIAFILES_DIRS = [
    os.path.join(os.path.dirname(BASE_DIR), "media"),
]

# Login
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/admin'


#from django.core.mail import send_mail
#send_mail(
#    'subject here',
#    'here is the message.',
#    'xyz@sowi.uni-stuttgart.de',
#    ['to@example.com'],
#    fail_silently=False,
#)
