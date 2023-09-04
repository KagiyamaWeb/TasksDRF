from pathlib import Path
from datetime import timedelta
from typing import Optional

from pydantic import BaseSettings, validator, BaseModel


PROJECT_DIR = Path(__file__).resolve().parent
BASE_DIR = PROJECT_DIR.parent

ALLOWED_HOSTS = ['*']


class EmailConnect(BaseModel):
    use_tls: bool = True
    host: Optional[str] = None
    host_user: Optional[str] = None
    host_password: Optional[str] = None
    port: int = 587


class PsqlConnect(BaseModel):
    engine: str = "django.db.backends.sqlite3"
    name: str = "db.sqlite3"
    host: Optional[str] = None
    port: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None

    @validator("name", pre=True, allow_reuse=True)
    def valid_name_db(cls, v):
        if v == "db.sqlite3":
            return str(BASE_DIR / v)
        return v


class RabbitConnect(BaseModel):
    host: str = "127.0.0.1"
    login: str = "guest"
    port: str = "5672"
    password: str = "guest"
    vhost: str = "/"


class Settings(BaseSettings):
    secret_key: str = 'django-insecure-ff2ldfal&gaes4d@p0c_#njp_!aq$2qz0%zmts&t^mm8wt)^*6'
    debug: bool = False
    rabbit_mq: RabbitConnect = RabbitConnect()
    email: EmailConnect = EmailConnect()
    db: PsqlConnect = PsqlConnect()
    web_address: str = "localhost:3000"
    protocol: str = "http"
    sentry_dsn: str = ""

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


settings = Settings()

SECRET_KEY = settings.secret_key
DEBUG = settings.debug


MY_APPS = (
    'Tasks',
    'Auth',
    'User'
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #
    'rest_framework',
    'django_filters',
    'drf_yasg',
    'djoser',
    *MY_APPS
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

ROOT_URLCONF = 'TasksDRF.urls'

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

WSGI_APPLICATION = 'TasksDRF.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': settings.db.engine,
        'NAME': settings.db.name,
        'USER': settings.db.user,
        'PASSWORD': settings.db.password,
        'HOST': settings.db.host,
        'PORT': settings.db.port,
    }
}

RABBIT_HOST = settings.rabbit_mq.host
RABBIT_PORT = settings.rabbit_mq.port
RABBIT_LOGIN = settings.rabbit_mq.login
RABBIT_PASSWORD = settings.rabbit_mq.password
RABBIT_VHOST = settings.rabbit_mq.vhost

CELERY_BROKER_URL = (
    f'amqp://{RABBIT_LOGIN}:{RABBIT_PASSWORD}@{RABBIT_HOST}/{RABBIT_VHOST}'
)
CELERY_ACCEPT_CONTENT = ('application/json',)
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

ROOT_URLCONF = 'TasksDRF.urls'
AUTH_USER_MODEL = 'User.User'

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=300),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    'ROTATE_REFRESH_TOKENS': True,
}

DJOSER = {
    #"SEND_ACTIVATION_EMAIL": True,
    #"EMAIL": {
    #    "activation": "User.email.ActivationEmail",
    #},
    'SERIALIZERS': {
        'user_create': 'Auth.serializers.UserRegistrationSerializer',
    },
}