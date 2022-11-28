import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

############################################
# Переменные окружения
if not os.environ.get('SECRET_KEY'):
    # Запуск сервера без докера (разработка или на виртуале)
    # Нет переменных окружения. Загружаем из файла.
    from dotenv import load_dotenv
    if os.path.exists(os.path.join(BASE_DIR, '.env')):
        load_dotenv(os.path.join(BASE_DIR, '.env'))


############################################
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')


############################################
# STRIPE
STRIPE_SK = os.environ.get('STRIPE_SK')
STRIPE_PK = os.environ.get('STRIPE_PK')


if os.environ.get('STATE') not in 'DEV':
    # PRODUCTION
    STRIPE_SUCCESS_URL = 'http://95.163.243.134:8137/success/'
    STRIPE_CANCEL_URL = 'http://95.163.243.134:8137/cancel/'
    DEBUG = False
    ALLOWED_HOSTS = ['95.163.243.134']
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    print(STATIC_ROOT)
else:
    # DEV
    STRIPE_SUCCESS_URL = 'http://localhost:8000/success/'
    STRIPE_CANCEL_URL = 'http://localhost:8000/cancel/'
    DEBUG = True
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'items.apps.ItemsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Asia/Omsk'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
