from pathlib import Path
import os
from datetime import timedelta
import environ


# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SECRET_KEY = "your-unique-django-secret-key-instructions-in-readme-file"

DEBUG = True

ALLOWED_HOSTS = [
    ".ngrok-free.app",
    "*"
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'https://*.ngrok-free.app',
    'https://*'
]

CORS_ALLOW_ALL_ORIGINS = True # Allow all origins (not recommended for production)
CORS_ALLOW_CREDENTIALS = True  # Allow cookies if needed

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # REST API Dependencies
    'rest_framework',
    'rest_framework_simplejwt',
    # Api 
    'api',
]

# API Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=6),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Luabla.urls'

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
                'Application.context_processors.selected_language',
                'Application.context_processors.total_notifications',
                'Application.context_processors.total_friend_requests',
                'Application.context_processors.languages_list'
            ],
        },
    },
]

WSGI_APPLICATION = 'Luabla.wsgi.application'

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        #'NAME': env('DATABASE_NAME'),
        # 'USER': env('DATABASE_USER'),
        # 'PASSWORD': env('DATABASE_PASSWORD'),
        # 'HOST': env('DATABASE_HOST'), # DB into a Docker container.
        # 'HOST': 'localhost', # Testing host, local for debug with ease and only for developing and testing 
        # 'PORT': env('DATABASE_PORT'),
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'luabladb.sqlite3'
    }
}

AUTH_USER_MODEL = 'Authentication.User'

# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login Default Redirection URL
LOGIN_URL = 'login'

# Emails sending settings
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER') 
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
