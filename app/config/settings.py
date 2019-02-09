"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.contrib import messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_DIR = os.path.dirname(BASE_DIR)

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
# 사용자가 업로드한 파일이 저장될 Base디렉토리(settings.MEDIA_URL)
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')

# 유저가 업로드한 파일에 접근하고자 할 때 prefix URL (settings.MEDIA_URL)
# FileField, MediaField의 URL이 아래 설정 기준으로 바
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = []

STATICFILES_DIRS = [
    STATIC_DIR,
]

# .secrets/base.json에 있는 내용을 읽어서
# parsing하여 파이썬 dict객체를 가져와 secrets변수에 할당
# loads는 문자열을 파싱하겠다는 뜻
# json.load는 파일객체를 넣을 수 있다. 아래처럼 파일 자체를 불러옴
secrets = json.load(open(os.path.join(SECRETS_DIR, 'base.json')))
FACEBOOK_APP_ID = secrets['FACEBOOK_APP_ID']
FACEBOOK_APP_SECRET = secrets['FACEBOOK_APP_SECRET']

# login_required 데코레이터에 의해
# 로그인 페이지로 이동해야 할 때, 그 이동할 URL또는 URL pattern name
LOGIN_URL = 'members:login'

# Application definition
AUTH_USER_MODEL = 'members.User'

# 로그인 유지시간이 지나면 자동으로 로그아웃 처리
SESSION_COOKEI_AGE = 20
# 로그인 상태에서 사용자가 액션을 취하면 갱신시킬건지?
SESSION_SAVE_EVERY_REQUEST = True
# 로그인상태에서 브라우저 종료후 다시 실행시 자동으로 로그아웃 시킴
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

INSTALLED_APPS = [
    # AppConfig클래스를사용
    'members.apps.MembersConfig',
    'posts.apps.PostsConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
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

ROOT_URLCONF = 'config.urls'

# 메세지모듈을 사용해서 태그별로 메세지를 출력할 때
# 부트스트랩에는 ERROR라는 값이 없고 danger이기 때문에 그것을 바꿔주는 코드
# 이렇게 해주어야 탬플릿에서 부트스트랩이 적용된다
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_DIR,
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

