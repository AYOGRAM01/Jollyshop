from pathlib import Path
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from decouple import config

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SECURITY
# =========================================================


SECRET_KEY = 'django-insecure-5evfv#c3z!f=@7by^4jdr0t)n4gnne8_57*_nytb9c*mfjhd%%'


DEBUG = config('DEBUG', default='True', cast=bool)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'jollyshop.onrender.com',
]


# =========================================================
# CLOUDINARY
# =========================================================

cloudinary.config(
    cloud_name=("dvfsjrfwn"),
    api_key=("492472243882776"),
    api_secret=("Q9NTEvzQnMCMi_4rIzRnU9RwKPk")
)


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'Mini_catalog',
    'cloudinary',
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =========================================================
# CLOUDINARY STORAGE
# =========================================================

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# =========================================================
# URL CONFIGURATION
# =========================================================

ROOT_URLCONF = 'ecommerce.urls'


# =========================================================
# TEMPLATES
# =========================================================

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


WSGI_APPLICATION = 'ecommerce.wsgi.application'


# =========================================================
# DATABASE
# =========================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =========================================================
# PASSWORD VALIDATION
# =========================================================

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


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'Mini_catalog/static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'


# =========================================================
# MEDIA FILES
# =========================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================================================
# AUTHENTICATION
# =========================================================

LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/register/'