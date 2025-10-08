import os
from datetime import timedelta
from pathlib import Path
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-secret-key-for-dev"
)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG",'False') == 'True')

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    "https://opalyachts-backend.onrender.com", 
]
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


# allauth settings / Render
ACCOUNT_EMAIL_VERIFICATION = "none"  

#store images 
# .env


AUTH_USER_MODEL='useraccount.User'
#it makes it possible to login(site_id)
SITE_ID=1

WEBSITE_URL='https://opalyachts-backend.onrender.com'

CHANNEL_LAYERS= {
    'default': {
        'BACKEND':'channels.layers.InMemoryChannelLayer'
    }
}

SIMPLE_JWT={
    "ACCESS_TOKEN_LIFETIME":timedelta(minutes=600),
    "REFRESH_TOKEN_LIFETIME":timedelta(days=7),
    "ROTATE_REFRESH_TOKEN":False,
    "BLACKLIST_AFTER_ROTATION":False,
    "UPDATE_LAST_LOGIN":True,
    "SIGNING_KEY":"complexkey",
    "ALGORITHM": "HS512",
}

ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_USERNAME_REQUIRED=True
ACCOUNT_AUTHENTICATION_METHOD='email'

REST_FRAMEWORK={
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES':(
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ]


}

CORS_ALLOWED_ORIGINS=[
    'http://127.0.0.1:8000',
    'http://127.0.0.1:3000',
    'https://opalyachts-backend.onrender.com'
]

CORS_ALLOW_ALL_ORIGINS=True

REST_AUTH={
    "USE_JWT":True,
    "JWT_AUTH_HTTPONLY":False
}



# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #for api
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    #for auth between django and rest
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'dj_rest_auth',
    'dj_rest_auth.registration',
    #allow data from frontend
    'corsheaders',
    #apps
    'chat',
    'useraccount',
    'property',
    # storing images

]

#deployment 
INSTALLED_APPS += ['cloudinary', 'cloudinary_storage']


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'opalyachts_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'opalyachts_backend.wsgi.application'
ASGI_APPLICATION = 'opalyachts_backend.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
'default': dj_database_url.config(
    default=os.environ.get(
            "DATABASE_URL",
            "postgresql://neondb_owner:npg_LnbxB7oSs8pQ@ep-muddy-boat-agqvuuwc-pooler.c-2.eu-central-1.aws.neon.tech/opalyachts"
        ),
        conn_max_age=600,
        ssl_require=True
)
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MEDIA_URL='/media/'
MEDIA_ROOT=BASE_DIR / 'media'
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_AUTH_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.CustomRegisterSerializer',
}
