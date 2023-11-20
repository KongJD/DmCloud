"""
Django settings for DmCloud project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '49c9hnv1_uwk!7ta^vt*hj4yr%mwdr*=nvw=t*ttu8x*h542g2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'baike',
    "species",
    "itools",
    'rest_framework',
    'rest_framework_simplejwt',
    "corsheaders",
    "django_elasticsearch_dsl",
    "django_elasticsearch_dsl_drf",
    "django_celery_results",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'DmCloud.urls'

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

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/5'  # 配置代理人，指定代理人将任务存到哪里,这里是redis的1号库
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'django-db'  # 结果
BROKER_TRANSPORT = 'redis'
CELERY_TASK_SERIALIZER = 'json'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYD_CONCURRENCY = 5  # 并发worker数
CELERYD_MAX_TASKS_PER_CHILD = 60  ## 每个worker最多执行万60个任务就会被销毁，可防止内存泄露
CELERY_ACKS_LATE = True  # 允许重试
CELERYD_FORCE_EXECV = True  # 可以让Celery更加可靠,只有当worker执行完任务后,才会告诉MQ,消息被消费，防治死锁

WSGI_APPLICATION = 'DmCloud.wsgi.application'
ASGI_APPLICATION = 'DmCloud.asgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=10),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=5),
    'UPDATE_LAST_LOGIN': True,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DMCloudDb',
        'USER': 'siteusra',
        'PASSWORD': 'dm20210120',
        'HOST': '192.168.100.10',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4'},
    },
    'db1': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testDb',
        'USER': 'siteusra',
        'PASSWORD': 'dm20210120',
        'HOST': '192.168.100.10',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4'},
    }

}

DATABASE_APPS_MAPPING = {
    "baike": 'default',
    "species": 'db1',
    "admin": "default",
    "auth": "default",
    "contenttypes": "default",
    "sessions": "default",
    "django_celery_results": "default",
    "itools": "default",
}

DATABASE_ROUTERS = ['DmCloud.database_router.DatabaseAppsRouter']

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': '127.0.0.1:9200'
    },
}