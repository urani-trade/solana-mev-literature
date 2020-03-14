""" NISQ Algorithm Zoo settings for main project. """

import os
from main.utils import extract_env_var


# -------------------------------------------------
# Define all the URLS and endpoints for the app.
# 
# Set DEBUG to True when running locally.
# ------------------------------------------------- 

DEBUG = False

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ['.now.sh', '.nisqalgorithmzoo.com']

data = extract_env_var()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

S3_BUCKET = data['S3_BUCKET']
STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
AWS_S3_BUCKET_NAME_STATIC = S3_BUCKET
STATIC_URL = "https://{}.s3.amazonaws.com/".format(S3_BUCKET)

ROOT_URLCONF = 'main.urls'
WSGI_APPLICATION = 'main.wsgi.application'


# -------------------------------------------------
# Load  data and env variables to be 
#  used in the app.
# ------------------------------------------------- 

data = extract_env_var()
SECRET_KEY = data['SECRET_KEY']
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# -------------------------------------------------
# This is where django discovers the different modules 
# that are part of the project.
# ------------------------------------------------- 

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'implementations.apps.ImplementationsConfig',
    'accounts.apps.AccountsConfig',
    'django_s3_storage',
]


# -------------------------------------------------
# Every time a request hits the Django server it runs 
# through the middleware.
# ------------------------------------------------- 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# -------------------------------------------------
# These are the settings for Django Rest Frameworks. 
# Now it accepts OAuth2 as authentication.
# ------------------------------------------------- 

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication', 
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


# -------------------------------------------------
# This specifies what authentication system 
# should be used.
# ------------------------------------------------- 

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', 
)


# -------------------------------------------------
# Define all the templates for DJANGO
# ------------------------------------------------- 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# -------------------------------------------------
# Database definitions and variables.
# ------------------------------------------------- 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': data['DB_NAME'],
        'USER': data['DB_USER'],
        'PASSWORD': data['DB_PASSWORD'],
        'HOST': data['DB_HOST'],
        'PORT': data['DB_PORT'],
    }
}


# -------------------------------------------------
# Define password validation for register.
# ------------------------------------------------- 

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


# -------------------------------------------------
# Email settings.
# ------------------------------------------------- 

SENDGRID_API_KEY = data['SENDGRID_API_KEY']
NQZ_EMAIL = data['NQZ_EMAIL']
ADMIN_EMAIL = data['ADMIN_EMAIL']
EMAIL_HOST = data['EMAIL_HOST']
EMAIL_PORT = data['EMAIL_PORT']
EMAIL_HOST_USER = data['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = NQZ_EMAIL
